from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import structlog

logger = structlog.get_logger()

class DataAnalyzer:
    """
    Data analysis tool for agents
    Performs statistical analysis, trend detection, and insights extraction
    """
    
    def __init__(self):
        self.data_cache: Dict[str, pd.DataFrame] = {}
    
    async def load_data(
        self,
        data: Any,
        data_id: str,
        format: str = "auto"
    ) -> pd.DataFrame:
        """
        Load data into DataFrame
        
        Args:
            data: Data to load (dict, list, or DataFrame)
            data_id: Identifier for caching
            format: Data format (auto, json, csv, dict)
        
        Returns:
            pandas DataFrame
        """
        try:
            if isinstance(data, pd.DataFrame):
                df = data
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                raise ValueError(f"Unsupported data type: {type(data)}")
            
            # Cache the data
            self.data_cache[data_id] = df
            
            logger.info("Data loaded", data_id=data_id, rows=len(df), cols=len(df.columns))
            
            return df
        
        except Exception as e:
            logger.error("Error loading data", error=str(e))
            raise
    
    async def analyze_statistics(
        self,
        data_id: str,
        columns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Perform statistical analysis
        
        Args:
            data_id: Identifier of loaded data
            columns: Specific columns to analyze (None for all)
        
        Returns:
            Statistical summary
        """
        try:
            df = self.data_cache.get(data_id)
            if df is None:
                raise ValueError(f"Data not found: {data_id}")
            
            # Select columns
            if columns:
                df = df[columns]
            
            # Calculate statistics
            stats = {
                "shape": {"rows": len(df), "columns": len(df.columns)},
                "columns": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "missing_values": df.isnull().sum().to_dict(),
                "numeric_summary": {}
            }
            
            # Numeric columns analysis
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                stats["numeric_summary"][col] = {
                    "mean": float(df[col].mean()),
                    "median": float(df[col].median()),
                    "std": float(df[col].std()),
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "q25": float(df[col].quantile(0.25)),
                    "q75": float(df[col].quantile(0.75))
                }
            
            logger.info("Statistics analyzed", data_id=data_id)
            
            return stats
        
        except Exception as e:
            logger.error("Error analyzing statistics", error=str(e))
            raise
    
    async def detect_trends(
        self,
        data_id: str,
        time_column: str,
        value_column: str
    ) -> Dict[str, Any]:
        """
        Detect trends in time series data
        
        Args:
            data_id: Identifier of loaded data
            time_column: Column with timestamps
            value_column: Column with values
        
        Returns:
            Trend analysis results
        """
        try:
            df = self.data_cache.get(data_id)
            if df is None:
                raise ValueError(f"Data not found: {data_id}")
            
            # Sort by time
            df = df.sort_values(time_column)
            
            # Calculate trend
            values = df[value_column].values
            trend = np.polyfit(range(len(values)), values, 1)
            
            # Calculate percentage change
            pct_change = ((values[-1] - values[0]) / values[0]) * 100 if values[0] != 0 else 0
            
            results = {
                "trend_direction": "increasing" if trend[0] > 0 else "decreasing",
                "trend_slope": float(trend[0]),
                "percentage_change": float(pct_change),
                "start_value": float(values[0]),
                "end_value": float(values[-1]),
                "data_points": len(values)
            }
            
            logger.info("Trends detected", data_id=data_id, direction=results["trend_direction"])
            
            return results
        
        except Exception as e:
            logger.error("Error detecting trends", error=str(e))
            raise
    
    async def find_correlations(
        self,
        data_id: str,
        columns: Optional[List[str]] = None,
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Find correlations between columns
        
        Args:
            data_id: Identifier of loaded data
            columns: Specific columns to analyze
            threshold: Minimum correlation coefficient to report
        
        Returns:
            Correlation analysis
        """
        try:
            df = self.data_cache.get(data_id)
            if df is None:
                raise ValueError(f"Data not found: {data_id}")
            
            # Select numeric columns
            if columns:
                df = df[columns]
            else:
                df = df.select_dtypes(include=[np.number])
            
            # Calculate correlations
            corr_matrix = df.corr()
            
            # Find significant correlations
            significant = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) >= threshold:
                        significant.append({
                            "column1": corr_matrix.columns[i],
                            "column2": corr_matrix.columns[j],
                            "correlation": float(corr_value),
                            "strength": self._interpret_correlation(abs(corr_value))
                        })
            
            # Sort by absolute correlation
            significant.sort(key=lambda x: abs(x["correlation"]), reverse=True)
            
            logger.info("Correlations found", data_id=data_id, count=len(significant))
            
            return {
                "significant_correlations": significant,
                "correlation_matrix": corr_matrix.to_dict()
            }
        
        except Exception as e:
            logger.error("Error finding correlations", error=str(e))
            raise
    
    def _interpret_correlation(self, value: float) -> str:
        """Interpret correlation strength"""
        if value >= 0.9:
            return "very strong"
        elif value >= 0.7:
            return "strong"
        elif value >= 0.5:
            return "moderate"
        elif value >= 0.3:
            return "weak"
        else:
            return "very weak"
    
    async def generate_insights(
        self,
        data_id: str
    ) -> List[str]:
        """
        Generate insights from data
        
        Args:
            data_id: Identifier of loaded data
        
        Returns:
            List of insights
        """
        insights = []
        
        try:
            # Get statistics
            stats = await self.analyze_statistics(data_id)
            
            # Insight: Data size
            insights.append(
                f"Dataset contains {stats['shape']['rows']} rows and {stats['shape']['columns']} columns"
            )
            
            # Insight: Missing values
            missing = stats['missing_values']
            missing_cols = [col for col, count in missing.items() if count > 0]
            if missing_cols:
                insights.append(
                    f"Found missing values in {len(missing_cols)} columns: {', '.join(missing_cols[:3])}"
                )
            
            # Insight: Numeric ranges
            for col, summary in stats['numeric_summary'].items():
                range_val = summary['max'] - summary['min']
                insights.append(
                    f"{col}: ranges from {summary['min']:.2f} to {summary['max']:.2f} (mean: {summary['mean']:.2f})"
                )
            
            logger.info("Insights generated", data_id=data_id, count=len(insights))
            
            return insights
        
        except Exception as e:
            logger.error("Error generating insights", error=str(e))
            return []


# Convenience functions for agents
async def analyze_data(data: Any, data_id: str = "default") -> Dict[str, Any]:
    """Analyze data and return statistics"""
    analyzer = DataAnalyzer()
    await analyzer.load_data(data, data_id)
    return await analyzer.analyze_statistics(data_id)

async def find_data_trends(
    data: Any,
    time_column: str,
    value_column: str
) -> Dict[str, Any]:
    """Find trends in time series data"""
    analyzer = DataAnalyzer()
    data_id = f"trends_{datetime.now().timestamp()}"
    await analyzer.load_data(data, data_id)
    return await analyzer.detect_trends(data_id, time_column, value_column)

async def get_data_insights(data: Any) -> List[str]:
    """Get insights from data"""
    analyzer = DataAnalyzer()
    data_id = f"insights_{datetime.now().timestamp()}"
    await analyzer.load_data(data, data_id)
    return await analyzer.generate_insights(data_id)
