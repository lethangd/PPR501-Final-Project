#!/usr/bin/env python3
"""
Student Data Crawler & Analyzer.

This module provides functionality to:
1. Crawl student data from backend API (XML)
2. Clean and normalize the data using Pandas
3. Perform statistical analysis (correlation, grouping, comparison)
4. Export results to Excel file with multiple sheets

Usage:
    python crawl_and_analyze.py --url http://localhost:8000/api/students --out output/students.xlsx


Author: PPR501 Team
Version: 1.0.0
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET

import pandas as pd
import requests

# Score columns used for analysis
SCORE_COLS: list[str] = ["math_score", "literature_score", "english_score"]

# Default configuration
# Use XML API by default
DEFAULT_URL: str = "http://localhost:8000/api/students"
DEFAULT_OUTPUT: str = "output/students.xlsx"

def _xml_text_or_none(el: Optional[ET.Element]) -> Optional[str]:
    if el is None or el.text is None:
        return None
    value = el.text.strip()
    return value or None


def crawl_students_xml(url: str) -> pd.DataFrame:
    """Crawl student data from XML API endpoint.

    The backend returns:
      <students><student>...</student></students>

    Args:
        url: XML API endpoint URL
             Example: "http://localhost:8000/api/students"

    Returns:
        pd.DataFrame: Raw data with English column names
    """

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)
    if root.tag != "students":
        raise RuntimeError(
            f"Unexpected XML root <{root.tag}> from {url}. "
            "Expected <students>."
        )

    rows: List[Dict[str, Any]] = []
    for student_el in root.findall("student"):
        row: Dict[str, Any] = {}
        for key in [
            "student_id",
            "last_name",
            "first_name",
            "email",
            "birth_date",
            "hometown",
            "math_score",
            "literature_score",
            "english_score",
        ]:
            row[key] = _xml_text_or_none(student_el.find(key))
        rows.append(row)

    return pd.DataFrame(rows)


def crawl_students(url: str) -> pd.DataFrame:
    """Crawl student data from XML API."""
    return crawl_students_xml(url)


def clean_students(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize student data.
    
    Performs the following cleaning operations:
    1. Replace empty strings with NA (missing values)
    2. Strip whitespace from string columns
    3. Parse birth_date as datetime objects
    4. Convert score columns to numeric type
    
    Args:
        df: Raw DataFrame from crawl_students_table()
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with proper data types
        
    Example:
        >>> raw = crawl_students_table(url)
        >>> cleaned = clean_students(raw)
        >>> print(cleaned.dtypes)
        student_id         string
        birth_date         object  (datetime.date)
        math_score        float64
        ...
    """
    # Work on a copy to avoid modifying original data
    df = df.copy()
    
    # Step 1: Normalize empty strings to pandas NA
    # This ensures consistent handling of missing values
    df = df.replace({"": pd.NA})
    
    # Step 2: Clean whitespace from string columns
    # Iterate through all columns and strip if string type
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype("string").str.strip()
    
    # Step 3: Parse date column
    # Use errors='coerce' to convert invalid dates to NaT (Not a Time)
    if "birth_date" in df.columns:
        df["birth_date"] = pd.to_datetime(
            df["birth_date"], 
            errors="coerce"
        ).dt.date
    
    # Step 4: Parse score columns as numeric
    # Use errors='coerce' to convert non-numeric values to NaN
    for col in SCORE_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df


def analyze(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Perform statistical analysis on student data.
    
    Generates the following analyses:
    1. Correlation between English and Math scores
    2. Descriptive statistics for English and Math scores
    3. English score statistics grouped by hometown
    4. Score difference (English - Math) per student
    
    Args:
        df: Cleaned DataFrame from clean_students()
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary of analysis results
            - "english_vs_math_corr": Correlation matrix
            - "english_vs_math_describe": Descriptive statistics
            - "hometown_vs_english": Grouped statistics by hometown
            - "english_minus_math": Score differences sorted
            
    Example:
        >>> results = analyze(cleaned_df)
        >>> print(results["english_vs_math_corr"])
                      english_score  math_score
        english_score      1.000000    0.023456
        math_score         0.023456    1.000000
    """
    results: Dict[str, pd.DataFrame] = {}
    
    # -------------------------------------------------------------------------
    # Analysis 1: English vs Math Correlation
    # -------------------------------------------------------------------------
    # Measures linear relationship between the two score columns
    # Value ranges from -1 (inverse) to 1 (direct correlation)
    
    if "english_score" in df.columns and "math_score" in df.columns:
        # Calculate Pearson correlation coefficient matrix
        corr = df[["english_score", "math_score"]].corr(numeric_only=True)
        results["english_vs_math_corr"] = corr
        
        # Descriptive statistics: count, mean, std, min, 25%, 50%, 75%, max
        desc = df[["english_score", "math_score"]].describe()
        results["english_vs_math_describe"] = desc
    
    # -------------------------------------------------------------------------
    # Analysis 2: Hometown vs English Score
    # -------------------------------------------------------------------------
    # Groups students by hometown and calculates English score statistics
    # Useful for comparing academic performance across regions
    
    if "hometown" in df.columns and "english_score" in df.columns:
        by_home = (
            df.groupby("hometown", dropna=False)["english_score"]
            .agg(
                count="count",    # Number of students
                mean="mean",      # Average score
                median="median",  # Middle value
                min="min",        # Lowest score
                max="max"         # Highest score
            )
            .sort_values(
                ["count", "mean"], 
                ascending=[False, False]  # Sort by count desc, then mean desc
            )
            .reset_index()
        )
        results["hometown_vs_english"] = by_home
    
    # -------------------------------------------------------------------------
    # Analysis 3: Score Difference (English - Math)
    # -------------------------------------------------------------------------
    # Shows which subject each student performs better in
    # Positive = better at English, Negative = better at Math
    
    if "english_score" in df.columns and "math_score" in df.columns:
        # Include student_id if available for identification
        if "student_id" in df.columns:
            diff = df[["student_id", "english_score", "math_score"]].copy()
        else:
            diff = df[["english_score", "math_score"]].copy()
        
        # Calculate the difference
        diff["english_minus_math"] = diff["english_score"] - diff["math_score"]
        
        # Sort by difference (highest English advantage first)
        results["english_minus_math"] = diff.sort_values(
            "english_minus_math", 
            ascending=False
        )
    
    return results


def main() -> None:
    """
    Main entry point for the crawler script.
    
    Workflow:
    1. Parse command line arguments
    2. Crawl student data (XML API preferred)
    3. Clean and normalize the data
    4. Perform statistical analysis
    5. Export results to Excel file
    6. Print summary to console
    
    Command Line Args:
        --url: URL of XML API
             (default: http://localhost:8000/api/students)
        --out: Output Excel file path
               (default: output/students.xlsx)
    """
    parser = argparse.ArgumentParser(
        description="Crawl students from the website and export Excel + analysis.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Use default settings
    python crawl_and_analyze.py
    
    # Specify custom URL and output
    python crawl_and_analyze.py --url http://localhost:8000/api/students --out results.xlsx
        """
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"XML API endpoint (default: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUTPUT,
        help=f"Output Excel file path (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()
    
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"🔍 Crawling data from: {args.url}")
    
    raw = crawl_students(args.url)
    print(f"✅ Crawled {len(raw)} students")
    
    cleaned = clean_students(raw)
    print("✅ Data cleaned and normalized")
    
    results = analyze(cleaned)
    print(f"✅ Generated {len(results)} analysis sheets")
    
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        # Write raw data
        raw.to_excel(writer, sheet_name="raw", index=False)
        
        # Write cleaned data
        cleaned.to_excel(writer, sheet_name="cleaned", index=False)
        
        # Write analysis results
        # Sheet names are limited to 31 characters in Excel
        for sheet, df in results.items():
            safe_sheet = sheet[:31]
            df.to_excel(writer, sheet_name=safe_sheet, index=True)
    
    print(f"\n📊 Saved: {out_path.resolve()}")
    print("\n📋 Excel Sheets Created:")
    print("   - raw: Original crawled data")
    print("   - cleaned: Cleaned and normalized data")
    for sheet in results.keys():
        print(f"   - {sheet[:31]}: Analysis results")
    
    # Print correlation coefficient if available
    if "english_vs_math_corr" in results:
        corr = results["english_vs_math_corr"].loc["english_score", "math_score"]
        print(f"\n📈 Correlation(english, math) = {corr:.4f}")


if __name__ == "__main__":
    main()

