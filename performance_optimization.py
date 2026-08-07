"""
Performance Optimization for Large-Scale Data Processing
========================================================

This module implements performance optimization techniques for handling  
100M+ transaction records efficiently.

Optimization Techniques:
1. Partitioning strategy
2. Bucketing
3. Predicate pushdown
4. Broadcast joins
5. File compaction
6. Caching strategies

Design Decisions:
- Partition by date for time-based queries
- Bucket by account_number for join optimization
- Use Delta Lake optimizations
- Broadcast small dimension tables
"""

import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, broadcast, date_format
from delta.tables import DeltaTable
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceOptimizer:
    """
    Handles performance optimization for Spark jobs.
    
    Features:
    - Partitioning
    - Bucketing
    - Join optimization
    - File compaction
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.spark = SparkSession.builder \
            .appName("PerformanceOptimizer") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.sql.adaptive.skewJoin.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .config("spark.sql.shuffle.partitions", str(self.config['performance']['partitions'])) \
            .config("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB") \
            .getOrCreate()
        
        self.performance_config = self.config['performance']
    
    def optimize_partitioning(self, df, partition_columns: list):
        """
        Optimize DataFrame partitioning.
        
        Args:
            df: Input DataFrame
            partition_columns: List of columns to partition by
            
        Returns:
            Repartitioned DataFrame
        """
        logger.info(f"Repartitioning by: {partition_columns}")
        
        # Repartition for better distribution
        df = df.repartition(self.performance_config['partitions'], *partition_columns)
        
        return df
    
    def apply_bucketing(self, df, bucket_columns: list, num_buckets: int):
        """
        Apply bucketing to DataFrame.
        
        Args:
            df: Input DataFrame
            bucket_columns: Columns to bucket by
            num_buckets: Number of buckets
            
        Returns:
            Bucketed DataFrame
        """
        if self.performance_config.get('enable_bucketing', False):
            logger.info(f"Bucketing by {bucket_columns} into {num_buckets} buckets")
            df = df.bucketBy(num_buckets, *bucket_columns)
        
        return df
    
    def optimize_joins(self, large_df, small_df, join_key: str):
        """
        Optimize joins using broadcast for small tables.
        
        Args:
            large_df: Large DataFrame
            small_df: Small DataFrame (will be broadcast if small enough)
            join_key: Join key column
            
        Returns:
            Joined DataFrame
        """
        broadcast_threshold = self.performance_config['broadcast_join_threshold']
        small_count = small_df.count()
        
        if small_count < broadcast_threshold:
            logger.info(f"Broadcasting small table ({small_count} rows)")
            small_df = broadcast(small_df)
        
        result = large_df.join(small_df, on=join_key, how="inner")
        return result
    
    def optimize_delta_table(self, table_path: str):
        """
        Optimize Delta table using OPTIMIZE and ZORDER.
        
        Args:
            table_path: Path to Delta table
        """
        logger.info(f"Optimizing Delta table: {table_path}")
        
        # Optimize: Compact small files
        self.spark.sql(f"OPTIMIZE delta.`{table_path}`")
        
        # Z-order: Co-locate related data
        zorder_columns = self.performance_config.get('bucket_columns', ['account_number'])
        zorder_clause = ", ".join(zorder_columns)
        self.spark.sql(f"OPTIMIZE delta.`{table_path}` ZORDER BY ({zorder_clause})")
        
        logger.info("Delta table optimization completed")
    
    def enable_predicate_pushdown(self, df):
        """
        Enable predicate pushdown for better query performance.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with predicate pushdown enabled
        """
        # Predicate pushdown is automatically enabled in Spark
        # This method documents the optimization
        logger.info("Predicate pushdown enabled (automatic in Spark)")
        return df
    
    def cache_strategically(self, df, cache_name: str = None):
        """
        Cache DataFrame if it will be reused multiple times.
        
        Args:
            df: Input DataFrame
            cache_name: Optional cache name
            
        Returns:
            Cached DataFrame
        """
        logger.info(f"Caching DataFrame: {cache_name}")
        df.cache()
        return df
    
    def optimize_write(self, df, output_path: str, partition_columns: list = None):
        """
        Optimize write operation with partitioning and file size control.
        
        Args:
            df: DataFrame to write
            output_path: Output path
            partition_columns: Columns to partition by
        """
        logger.info(f"Writing optimized data to: {output_path}")
        
        writer = df.write.format("delta").mode("overwrite")
        
        if partition_columns:
            writer = writer.partitionBy(*partition_columns)
        
        writer.option("delta.autoOptimize.optimizeWrite", "true") \
              .option("delta.autoOptimize.autoCompact", "true") \
              .option("maxRecordsPerFile", "1000000") \
              .save(output_path)
        
        logger.info("Optimized write completed")
    
    def analyze_table(self, table_path: str):
        """
        Analyze table statistics for query optimization.
        
        Args:
            table_path: Path to Delta table
        """
        logger.info(f"Analyzing table: {table_path}")
        self.spark.sql(f"ANALYZE TABLE delta.`{table_path}` COMPUTE STATISTICS FOR ALL COLUMNS")
        logger.info("Table analysis completed")


class OptimizedTransformation:
    """
    Example of optimized transformation using all techniques.
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize optimizer."""
        self.optimizer = PerformanceOptimizer(config_path)
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def optimized_silver_to_gold(self):
        """
        Optimized version of Silver to Gold transformation.
        """
        silver_path = f"{self.config['storage']['silver_path']}/transactions"
        gold_path = f"{self.config['storage']['gold_path']}/risk_transactions"
        
        # Read with predicate pushdown
        silver_df = self.optimizer.spark.read.format("delta").load(silver_path)
        
        # Filter early (predicate pushdown)
        recent_df = silver_df.filter(
            col("load_date") >= date_format(col("transaction_date"), "yyyy-MM-dd")
        )
        
        # Optimize partitioning
        recent_df = self.optimizer.optimize_partitioning(
            recent_df,
            ["load_date", "source_system"]
        )
        
        # Read customer master (small table - will be broadcast)
        customer_df = self.optimizer.spark.read.format("delta").load(
            f"{self.config['storage']['gold_path']}/customer_master"
        ).filter(col("is_current") == True)
        
        # Optimized join
        enriched_df = self.optimizer.optimize_joins(
            recent_df,
            customer_df,
            "account_number"
        )
        
        # Optimized write
        self.optimizer.optimize_write(
            enriched_df,
            gold_path,
            ["load_date", "risk_level", "transaction_month"]
        )
        
        # Optimize Delta table
        self.optimizer.optimize_delta_table(gold_path)
        
        # Analyze for query optimization
        self.optimizer.analyze_table(gold_path)
        
        logger.info("Optimized transformation completed")


if __name__ == "__main__":
    """
    Entry point for performance optimization.
    
    Usage:
        python performance_optimization.py
    """
    optimizer = PerformanceOptimizer()
    logger.info("Performance optimizer initialized")
