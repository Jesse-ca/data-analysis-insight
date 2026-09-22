#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel解析脚本 - 固定使用pandas
用法: python parse_excel.py <excel_file_path>
输出: JSON格式的解析结果
"""

import pandas as pd
import json
import sys
import os

def parse_excel(file_path):
    """
    解析Excel文件，返回结构化数据
    
    Args:
        file_path: Excel文件路径
        
    Returns:
        dict: 包含sheet信息、数据结构、统计信息的字典
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return {"error": f"文件不存在: {file_path}"}
    
    # 检查文件扩展名
    if not file_path.endswith(('.xlsx', '.xls')):
        return {"error": "文件格式不支持，请上传.xlsx或.xls文件"}
    
    try:
        # 读取所有sheet
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names
        
        result = {
            "file_path": file_path,
            "sheet_names": sheet_names,
            "sheet_count": len(sheet_names),
            "sheets": {}
        }
        
        # 解析每个sheet
        for sheet_name in sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # 基本信息
            sheet_info = {
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "null_counts": {col: int(count) for col, count in df.isnull().sum().items()},
                "sample_data": json.loads(df.head(5).to_json(orient="records", date_format="iso"))
            }
            
            # 数值列统计
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                sheet_info["numeric_stats"] = {}
                for col in numeric_cols:
                    sheet_info["numeric_stats"][col] = {
                        "min": float(df[col].min()) if not pd.isna(df[col].min()) else None,
                        "max": float(df[col].max()) if not pd.isna(df[col].max()) else None,
                        "mean": float(df[col].mean()) if not pd.isna(df[col].mean()) else None,
                        "sum": float(df[col].sum()) if not pd.isna(df[col].sum()) else None
                    }
            
            # 分类列统计
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                sheet_info["categorical_stats"] = {}
                for col in categorical_cols:
                    value_counts = df[col].value_counts().head(10)
                    sheet_info["categorical_stats"][col] = {
                        "unique_count": int(df[col].nunique()),
                        "top_values": {str(k): int(v) for k, v in value_counts.items()}
                    }
            
            # 完整数据（最多返回10000行）
            MAX_ROWS = 10000
            if len(df) > MAX_ROWS:
                sheet_info["data"] = json.loads(df.head(MAX_ROWS).to_json(orient="records", date_format="iso"))
                sheet_info["data_truncated"] = True
                sheet_info["total_rows"] = len(df)
            else:
                sheet_info["data"] = json.loads(df.to_json(orient="records", date_format="iso"))
                sheet_info["data_truncated"] = False
            
            result["sheets"][sheet_name] = sheet_info
        
        return result
        
    except Exception as e:
        return {"error": f"解析Excel文件失败: {str(e)}"}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "请提供Excel文件路径"}, ensure_ascii=False))
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = parse_excel(file_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
