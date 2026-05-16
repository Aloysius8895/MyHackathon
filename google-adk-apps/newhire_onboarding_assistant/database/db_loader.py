"""
Database connection and data loader module for PostgreSQL
Replaces the file-based MockDataLoader with database queries
"""

import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Optional, Any
from dotenv import load_dotenv
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DatabaseLoader:
    """Load JSON data from PostgreSQL database instead of files"""
    
    def __init__(self):
        """Initialize database connection parameters"""
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT', 5432),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        self._connection = None
        
    def _get_connection(self):
        """Get or create database connection"""
        try:
            if self._connection is None or self._connection.closed:
                self._connection = psycopg2.connect(**self.db_config)
            return self._connection
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
            
    def load_data(self, path: str) -> Dict[str, Any]:
        """
        Load JSON data from database based on path
        
        Args:
            path: Path in format "category/filename.json" (e.g., "codebase/repositories.json")
            
        Returns:
            Dict: JSON data from database
        """
        try:
            # Parse the path to extract category and filename
            parts = path.split('/')
            if len(parts) != 2:
                raise ValueError(f"Invalid path format: {path}. Expected 'category/filename.json'")
                
            category = parts[0]
            filename = parts[1]
            
            # Query the database
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT data 
                    FROM json_documents 
                    WHERE category = %s AND filename = %s
                    LIMIT 1
                """
                cursor.execute(query, (category, filename))
                result = cursor.fetchone()
                
                if result:
                    # The data is already in JSON format in the database
                    return result['data']
                else:
                    logger.warning(f"No data found for category='{category}', filename='{filename}'")
                    return {}
                    
        except Exception as e:
            logger.error(f"Failed to load data from database: {str(e)}")
            # Return empty dict to maintain compatibility
            return {}
            
    def load_data_by_category(self, category: str) -> Dict[str, Any]:
        """
        Load all JSON data for a specific category
        
        Args:
            category: Category name (e.g., "teams", "codebase", "documentation")
            
        Returns:
            Dict: All JSON data for the category
        """
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT filename, data 
                    FROM json_documents 
                    WHERE category = %s
                """
                cursor.execute(query, (category,))
                results = cursor.fetchall()
                
                # Combine all results into a single dict
                combined_data = {}
                for row in results:
                    combined_data[row['filename']] = row['data']
                    
                return combined_data
                
        except Exception as e:
            logger.error(f"Failed to load category data from database: {str(e)}")
            return {}
            
    def search_all_data(self, search_term: str) -> list:
        """
        Search across all JSON data in the database
        
        Args:
            search_term: Term to search for
            
        Returns:
            List: Matching records with category, filename, and relevant data
        """
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Use PostgreSQL's JSONB search capabilities
                query = """
                    SELECT category, subcategory, filename, data
                    FROM json_documents 
                    WHERE data::text ILIKE %s
                """
                cursor.execute(query, (f'%{search_term}%',))
                results = cursor.fetchall()
                
                return results
                
        except Exception as e:
            logger.error(f"Failed to search database: {str(e)}")
            return []
            
    def __del__(self):
        """Close database connection when object is destroyed"""
        if self._connection and not self._connection.closed:
            self._connection.close()
