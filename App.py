import datetime as dt
import calendar
from datetime import date, timedelta
import os
import re
import difflib
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title='TRACKING KPI ĐDKD - SS Trương Thanh Tân ',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='collapsed',
)

# ====================== LOGO ======================
logo_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 158.15 61.91" width="130" height="50"><title>Masan Group logo</title><path d="M490.29,502.16s17.83-12.81,45.76-12.93c25.9-.11,30.18,8.14,38,10.79,0,0-3.8,5.82-5.78,9.63s-13.32,17.93-26.5,22.21c0,0,18.71-15.72,21.55-27.57,0,0-26.87-20.43-73.26-1.92" transform="translate(-432.92 -481.05)" style="fill:#f36f21"/><path d="M521.55,489.11c42-10.64,59.59,9.56,59.59,9.56A60.39,60.39,0,0,1,561,521.3c11.28-1.28,21.79-13,24-16.69s6.16-9.17,6.16-9.17c-7.12-3.22-13.13-12-35.93-14.22-16.3-1.59-33.6,7.88-33.6,7.88" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M454.12,528V512.92a58.92,58.92,0,0,1-.15-6.31l-.06,0-7.1,21.11h-3.41l-7.25-21h-.09c0,2.33.1,5.52.09,6.28v15h-3.24V502.39h4.8L445.1,524h.07l7.17-21.31h5V528Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M465.15,515c.21-1.42.7-3.56,4.21-3.58,2.94,0,4.35,1,4.37,3s-.87,2.12-1.62,2.19l-5.11.65c-5.13.67-5.58,4.26-5.57,5.81,0,3.16,2.42,5.3,5.8,5.29a8.32,8.32,0,0,0,6.64-3c.12,1.42.55,2.82,3.3,2.81a6.24,6.24,0,0,0,1.69-.36v-2.26a4.84,4.84,0,0,1-1,.14c-.63,0-1-.3-1-1.09l-.05-10.6c0-4.73-5.37-5.13-6.85-5.13-4.54,0-7.47,1.76-7.6,6.17Zm8.42,6.37c0,2.48-2.85,4.35-5.74,4.36-2.35,0-3.38-1.17-3.39-3.19,0-2.32,2.42-2.8,4-3,3.86-.52,4.64-.78,5.15-1.18Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M492.47,514.47c0-1.17-.47-3.12-4.44-3.1-1,0-3.7.34-3.7,2.64,0,1.53,1,1.88,3.4,2.46l3.14.77c3.89.94,5.27,2.35,5.27,4.87,0,3.83-3.15,6.14-7.37,6.16-7.39,0-7.94-4.21-8-6.44h3c.11,1.45.55,3.78,5,3.75,2.24,0,4.27-.89,4.26-3,0-1.47-1-2-3.72-2.63l-3.65-.88c-2.59-.62-4.31-1.91-4.34-4.46,0-4.09,3.39-6,7.05-6,6.66,0,7.17,4.87,7.17,5.78Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M502.6,514.75c.2-1.42.68-3.58,4.2-3.6,2.91,0,4.33,1.06,4.33,3s-.86,2.13-1.61,2.18l-5.1.66c-5.11.65-5.57,4.27-5.56,5.79,0,3.19,2.41,5.31,5.79,5.31a8.34,8.34,0,0,0,6.63-3c.11,1.41.53,2.83,3.28,2.8a5.87,5.87,0,0,0,1.68-.35l0-2.26a6.5,6.5,0,0,1-1,.15c-.62,0-1-.32-1-1.1l0-10.61c0-4.72-5.35-5.11-6.83-5.11-4.53,0-7.44,1.76-7.56,6.16Zm8.36,6.49c0,2.47-2.82,4.36-5.74,4.37-2.35,0-3.37-1.18-3.39-3.18,0-2.34,2.44-2.8,4-3,3.87-.51,4.65-.8,5.14-1.2Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M534.55,527.71h-3v-11.5c-.13-3.2-1.07-4.83-4.13-4.81-1.77,0-4.88,1.15-4.7,6.15v10.16h-3.24l-.07-18.56h2.72l0,2.66h.07a6.85,6.85,0,0,1,5.67-3.19c2.91,0,6.58,1.15,6.6,6.45Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M468,533.85a1.19,1.19,0,0,1,.07.34.6.6,0,0,1-.19.46.81.81,0,0,1-.51.21l-.54-.18q-.45-.15-.75-.23a2.37,2.37,0,0,0-.59-.08,2.27,2.27,0,0,0-1.47.49,3.1,3.1,0,0,0-.92,1.27,4.89,4.89,0,0,0-.35,1.64,5.25,5.25,0,0,0,.56,2.41,2.27,2.27,0,0,0,1.91,1.26.77.77,0,0,1,.27,0l.43-.06.37-.1.37-.15L467,541a1,1,0,0,1,.4-.11.54.54,0,0,1,.42.19.69.69,0,0,1,.17.48,1,1,0,0,1-.82,1,5.35,5.35,0,0,1-1.69.27,4.1,4.1,0,0,1-2.28-.63,4.15,4.15,0,0,1-1.5-1.71,5.52,5.52,0,0,1-.55-2.35,7.3,7.3,0,0,1,.25-1.93,5,5,0,0,1,.76-1.63,3.74,3.74,0,0,1,1.34-1.14,4.33,4.33,0,0,1,1.91-.45,4.73,4.73,0,0,1,1.68.27,1.72,1.72,0,0,1,.91.62" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M470.75,537.9a4.78,4.78,0,0,0,.63,2.45,2.13,2.13,0,0,0,2,1.1,2.3,2.3,0,0,0,1.48-.48,2.78,2.78,0,0,0,.88-1.28,5.69,5.69,0,0,0,.31-1.78,5.11,5.11,0,0,0-.3-1.78,2.94,2.94,0,0,0-.89-1.29,2.21,2.21,0,0,0-1.44-.48,2.3,2.3,0,0,0-1.44.46,2.82,2.82,0,0,0-.91,1.27,5.12,5.12,0,0,0-.31,1.82m-1.59,0a5.74,5.74,0,0,1,.54-2.53,4.26,4.26,0,0,1,1.51-1.76,4,4,0,0,1,4.42.06,4.39,4.39,0,0,1,1.47,1.8,5.8,5.8,0,0,1,.51,2.43,5.89,5.89,0,0,1-.51,2.46,4.25,4.25,0,0,1-1.47,1.79,4.11,4.11,0,0,1-4.49,0,4.31,4.31,0,0,1-1.48-1.8,5.85,5.85,0,0,1-.51-2.44" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M479.44,534.07a.79.79,0,0,1,.21-.58.7.7,0,0,1,.52-.21.73.73,0,0,1,.53.21.78.78,0,0,1,.22.59v.14l0,0a3,3,0,0,1,1.13-.91,3.31,3.31,0,0,1,1.43-.32,3.46,3.46,0,0,1,1.63.4,3,3,0,0,1,1.21,1.21,4,4,0,0,1,.46,2V542a.68.68,0,0,1-.22.54.77.77,0,0,1-.53.19.73.73,0,0,1-.51-.19.69.69,0,0,1-.21-.53v-5.36a2.16,2.16,0,0,0-.65-1.67,2.21,2.21,0,0,0-1.55-.6,2.32,2.32,0,0,0-1.09.26,2,2,0,0,0-.82.79,2.41,2.41,0,0,0-.31,1.25v5.05a.81.81,0,0,1-.2.59.68.68,0,0,1-.51.21.74.74,0,0,1-.54-.22.77.77,0,0,1-.23-.58Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M488.69,541.75a1.05,1.05,0,0,1-.44-.77.7.7,0,0,1,.2-.49.64.64,0,0,1,.49-.21,1,1,0,0,1,.46.13,6.25,6.25,0,0,1,.57.37,3.06,3.06,0,0,0,.49.31,3,3,0,0,0,1.34.36,2.88,2.88,0,0,0,1.37-.32,1.06,1.06,0,0,0,.6-1A1.24,1.24,0,0,0,493,539a9.34,9.34,0,0,0-1.39-.65q-1-.4-1.55-.68a3.05,3.05,0,0,1-1-.79,1.94,1.94,0,0,1-.42-1.28,2.36,2.36,0,0,1,.39-1.31,2.79,2.79,0,0,1,1.11-1,4,4,0,0,1,1.64-.4,5,5,0,0,1,1.71.3,3.57,3.57,0,0,1,1.22.66,1.1,1.1,0,0,1,.38.74.65.65,0,0,1-.21.47.78.78,0,0,1-.5.23,4.06,4.06,0,0,1-.89-.41c-.39-.22-.67-.38-.86-.46a1.78,1.78,0,0,0-.69-.15,2,2,0,0,0-1.28.35,1.16,1.16,0,0,0-.46.86,1.34,1.34,0,0,0,.42.75,2.92,2.92,0,0,0,.78.52q.44.2,1.07.41c.42.14.71.25.87.32a3.77,3.77,0,0,1,1.54,1,2.2,2.2,0,0,1,.47,1.42,2.72,2.72,0,0,1-.42,1.37,2.86,2.86,0,0,1-1.19,1,4.49,4.49,0,0,1-2,.41,4.67,4.67,0,0,1-3.14-1.06" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M496.81,533.76a.74.74,0,0,1,.21-.56.71.71,0,0,1,.52-.21.74.74,0,0,1,.53.2.73.73,0,0,1,.22.56V539a2.75,2.75,0,0,0,.58,1.85,2.16,2.16,0,0,0,1.74.69q2.38,0,2.38-2.53v-5.22a.74.74,0,0,1,.21-.56.71.71,0,0,1,.51-.21.74.74,0,0,1,.53.2.73.73,0,0,1,.22.56v5.3a4.35,4.35,0,0,1-.4,1.86,3.14,3.14,0,0,1-1.27,1.38,4.23,4.23,0,0,1-2.22.53,4,4,0,0,1-2.11-.51,3.14,3.14,0,0,1-1.25-1.37,4.36,4.36,0,0,1-.4-1.88Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M506.53,533.81a.7.7,0,0,1,.22-.53.76.76,0,0,1,.54-.21.68.68,0,0,1,.51.2.84.84,0,0,1,.2.61v.3h.94a2.69,2.69,0,0,1,2.29-1.15,2.75,2.75,0,0,1,2.4,1.62,3.7,3.7,0,0,1,1.29-1.26,3.26,3.26,0,0,1,1.53-.36,3,3,0,0,1,1.52.44,3,3,0,0,1,1.1,1.21,3.92,3.92,0,0,1,.41,1.84v5.58a.74.74,0,0,1-.22.57.74.74,0,0,1-.53.21.7.7,0,0,1-.5-.22.76.76,0,0,1-.22-.56v-5.54a2.57,2.57,0,0,0-.27-1.21,1.78,1.78,0,0,0-.72-.76,2.08,2.08,0,0,0-1-.25,2.2,2.2,0,0,0-1.51.53,2.14,2.14,0,0,0-.6,1.69v5.5a.62.62,0,0,1-.22.51.8.8,0,0,1-.53.18.75.75,0,0,1-.5-.18.63.63,0,0,1-.22-.5v-5.34a2.48,2.48,0,0,0-.63-1.87,2.18,2.18,0,0,0-1.57-.6,2.85,2.85,0,0,0-1.12.26,1.84,1.84,0,0,0-.8.74,2.45,2.45,0,0,0-.3,1.28v5.57a.75.75,0,0,1-.22.57.73.73,0,0,1-.52.21.7.7,0,0,1-.51-.22.75.75,0,0,1-.22-.56Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M522.43,537.42h5.42a3.31,3.31,0,0,0-.7-2.13,2.38,2.38,0,0,0-1.86-.83,2.53,2.53,0,0,0-1.94.78,3.25,3.25,0,0,0-.79,2.18m-1.59.47a6.14,6.14,0,0,1,.56-2.34,4.52,4.52,0,0,1,1.46-1.79,3.92,3.92,0,0,1,4.43,0,4.44,4.44,0,0,1,1.49,1.78,5.34,5.34,0,0,1,.53,2.31q0,.78-.88.78h-6a3.22,3.22,0,0,0,.41,1.62,2.5,2.5,0,0,0,1.05,1,3.23,3.23,0,0,0,1.46.33,3.91,3.91,0,0,0,2.58-1,1.26,1.26,0,0,1,.6-.29.49.49,0,0,1,.41.2.78.78,0,0,1,.15.47.9.9,0,0,1-.23.58,4.46,4.46,0,0,1-1.5,1,5.2,5.2,0,0,1-2.09.42,4.42,4.42,0,0,1-2-.44,3.84,3.84,0,0,1-1.39-1.17,5,5,0,0,1-.77-1.58,6.65,6.65,0,0,1-.26-1.72l0-.06v0" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/><path d="M531,534a.83.83,0,0,1,.21-.59.69.69,0,0,1,.52-.22.72.72,0,0,1,.53.22.81.81,0,0,1,.22.6v.81h0a4.3,4.3,0,0,1,.87-1.13,1.77,1.77,0,0,1,1.13-.53.85.85,0,0,1,.59.23.76.76,0,0,1,.26.58.69.69,0,0,1-.26.6,2.4,2.4,0,0,1-.76.33,3.19,3.19,0,0,0-.65.23,2.54,2.54,0,0,0-1.2,2.4v4.66a.84.84,0,0,1-.2.6.68.68,0,0,1-.51.21.73.73,0,0,1-.54-.22.86.86,0,0,1-.22-.63Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/></svg>
"""

# ====================== CSS ======================
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(90deg, #1a365d 0%, #2b6cb0 100%);
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.12);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .main-header .logo {
        flex-shrink: 0;
        background: white;
        border-radius: 8px;
        padding: 6px 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: visible;
        min-width: 140px;
        min-height: 52px;
    }
    .main-header .logo svg {
        display: block;
        width: 130px;
        height: 50px;
        max-width: 100%;
    }
    .main-header .title-block { flex: 1; text-align: center; }
    .main-header h1 {
        margin: 0;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    .main-header h2 {
        margin: 2px 0 0 0;
        font-size: 12px;
        font-weight: 600;
        color: #fefcbf;
        letter-spacing: 0.3px;
    }
    
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column;
            text-align: center;
            padding: 8px;
        }
        .main-header h1 { font-size: 16px; }
        .main-header h2 { font-size: 11px; }
        
        .timegone-container {
            padding: 8px !important;
        }
        .timegone-title {
            font-size: 11px !important;
        }
        .timegone-grid {
            gap: 6px !important;
        }
        .timegone-item {
            font-size: 11px !important;
            padding: 4px 6px !important;
        }
    }
    
    .filter-label {
        font-weight: 700 !important;
        color: #c53030 !important;
        font-size: 11px !important;
        margin-bottom: 2px;
    }
    /* Mobile: ẩn caret, không chặn click (để dropdown/calendar vẫn mở) */
    [data-baseweb="select"] input,
    [data-testid="stSelectbox"] input,
    [data-testid="stMultiSelect"] input,
    [data-testid="stDateInput"] input {
        caret-color: transparent !important;
        user-select: none !important;
        -webkit-user-select: none !important;
    }
    .note-box {
        background: #f0f4f8;
        border: 1px solid #d1d5db;
        border-left: 5px solid #034ea2;
        padding: 14px 18px;
        border-radius: 8px;
        margin-top: 12px;
        font-size: 13px;
        line-height: 1.6;
        color: #1a202c;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    [data-testid="stPopover"] button {
        color: #e53e3e !important;
        font-weight: 900 !important;
        font-size: 13px !important;
    }
    
    footer {visibility: hidden;}
    #MainMenu, header {visibility: visible !important;}

    /* Multiselect cho phép gõ tìm — không khóa caret */
    div[data-baseweb="select"] input {
        caret-color: auto;
    }
    
    .custom-kpi-table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #bce2f5 !important;
        font-family: sans-serif;
        font-size: 11px;
        background-color: #ffffff;
    }
    .custom-kpi-table th {
        background-color: #1a365d !important;
        color: #ffffff !important;
        font-weight: bold !important;
        text-align: center !important;
        border: 1px solid #90cdf4 !important;
        padding: 6px 5px;
        white-space: nowrap;
    }
    .custom-kpi-table td {
        border: 1px solid #bce2f5 !important;
        padding: 5px 6px;
    }
    .custom-kpi-table tbody tr:nth-child(even) td:not([data-colored="1"]) {
        background-color: #e6f4fc !important;
    }
    .custom-kpi-table tbody tr:nth-child(odd) td:not([data-colored="1"]) {
        background-color: #ffffff !important;
    }
    .custom-kpi-table tbody tr.row-total td.row-total-cell,
    .custom-kpi-table tbody tr.row-total td:not([data-colored="1"]) {
        background-color: #1a365d !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        border-color: #2b6cb0 !important;
    }
    .custom-kpi-table tbody tr.row-total td {
        font-weight: 900 !important;
    }

    .custom-kpi-table td {
        text-align: center !important;
    }
    /* Cột % — tô màu theo rule KPI */
    .custom-kpi-table td.pct-red {
        background-color: #fed7d7 !important;
        color: #742a2a !important;
        font-weight: 700 !important;
    }
    .custom-kpi-table td.pct-green {
        background-color: #c6f6d5 !important;
        color: #22543d !important;
        font-weight: 700 !important;
    }
    .custom-kpi-table td.pct-purple {
        background-color: #e9d8fd !important;
        color: #553c9a !important;
        font-weight: 700 !important;
    }
    /* Tea battle — Chưa Đạt scale */
    .custom-kpi-table td.chua-low {
        background-color: #c6f6d5 !important;
        color: #22543d !important;
        font-weight: 900 !important;
    }
    .custom-kpi-table td.chua-mid {
        background-color: #fbd38d !important;
        color: #7b341e !important;
        font-weight: 900 !important;
    }
    .custom-kpi-table td.chua-high {
        background-color: #fc8181 !important;
        color: #742a2a !important;
        font-weight: 900 !important;
    }
    /* Tea battle — SỐ SUẤT text color */
    .custom-kpi-table td.suat-ok {
        color: #228b22 !important;
        font-weight: 900 !important;
    }
    .custom-kpi-table td.suat-rot {
        color: #c53030 !important;
        font-weight: 900 !important;
    }
    /* VIP KO ĐH */
    .custom-kpi-table td.vip-1 {
        background-color: #fed7d7 !important; color: #742a2a !important; font-weight: 700 !important;
    }
    .custom-kpi-table td.vip-2 {
        background-color: #feb2b2 !important; color: #822727 !important; font-weight: 700 !important;
    }
    .custom-kpi-table td.vip-3 {
        background-color: #fc8181 !important; color: #742a2a !important; font-weight: 800 !important;
    }
    .custom-kpi-table td.vip-4 {
        background-color: #c53030 !important; color: #ffffff !important; font-weight: 900 !important;
    }
    .custom-kpi-table tbody tr.row-total td:not([data-colored="1"]),
    .custom-kpi-table tbody tr.row-total td.row-total-cell {
        background-color: #1a365d !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        border-color: #2b6cb0 !important;
    }
    .custom-kpi-table tbody tr.row-total td:not([data-colored="1"]) {
        background-color: #1a365d !important;
        color: #ffffff !important;
        font-weight: 900 !important;
    }

    /* MBS group cards - responsive */
    .mbs-card-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-bottom: 12px;
    }
    .mbs-card {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        min-height: 0;
    }
    .mbs-card-title {
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 4px;
        line-height: 1.3;
    }
    .mbs-card-kh {
        font-size: 20px;
        font-weight: 800;
        line-height: 1.2;
    }
    .mbs-card-kh span {
        font-size: 13px;
        font-weight: 600;
        color: #718096;
    }
    .mbs-card-pct {
        font-size: 11px;
        color: #718096;
        margin: 2px 0 6px 0;
    }
    .mbs-card-footer {
        border-top: 1px solid #e2e8f0;
        padding-top: 6px;
        font-size: 11px;
        color: #4a5568;
        line-height: 1.4;
    }
    @media (max-width: 768px) {
        .mbs-card-grid {
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }
        .mbs-card {
            padding: 8px 10px;
            border-radius: 8px;
        }
        .mbs-card-title { font-size: 10px; margin-bottom: 2px; }
        .mbs-card-kh { font-size: 16px; }
        .mbs-card-kh span { font-size: 11px; }
        .mbs-card-pct { font-size: 10px; margin: 1px 0 4px 0; }
        .mbs-card-footer { font-size: 10px; padding-top: 4px; }
    }
    @media (max-width: 400px) {
        .mbs-card-grid {
            grid-template-columns: 1fr;
            gap: 6px;
        }
        .mbs-card { padding: 8px 10px; }
        .mbs-card-kh { font-size: 18px; }
    }


    .kpi-report-title {
        color: #034ea2 !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        text-align: center !important;
        margin-bottom: 4px !important;
    }
    div[data-testid="stCaptionContainer"] {
        text-align: center !important;
    }

</style>
""",
    unsafe_allow_html=True,
)


def render_metric_card(label, value):
  st.markdown(
      f"""
    <div style="background: #ebf8ff; border: 1px solid #bee3f8; border-radius: 6px; padding: 8px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.04); margin-bottom: 6px;">
        <div style="color: #c53030; font-weight: 800; font-size: 0.95rem; margin-bottom: 2px;">{label}</div>
        <div style="color: #c53030; font-weight: 800; font-size: 1.5rem;">{value}</div>
    </div>
    """,
      unsafe_allow_html=True,
  )


# ====================== ĐƯỜNG DẪN ======================
DATA_DIR = 'data'


# ====================== THÁNG BÁO CÁO ======================
# data/Thang09 | data/Thang10 — chọn tháng → load data + rule KPI 1–8
MONTH_OPTIONS = {
    'Thang09': {
        'label': 'Tháng 09/2026',
        'year': 2026, 'month': 9,
        'folder': 'Thang09',
        # Doc quản trị T09: ASO Total Chanté (toàn nhãn)
        'aso_focus_pat': r'chant[eé]|chante',
        'aso_focus_name': 'ASO Chanté - Trận Xanh (Total nhãn Chanté)',
        # Omachi VÀ Trộn
        'aso_focus2_pat': r'(?=.*omachi)(?=.*tr[oộ]n)|omachi.*tr[oộ]n|tr[oộ]n.*omachi|m[iì]\s*tr[oộ]n\s*omachi|mi\s*tron\s*omachi',
        'aso_focus2_name': 'ASO Omachi Trộn - Trận Vàng',
        # ASO Tea ON: Tea/Trà/ô long, >=12 chai
        'pc_on_pat': r'tea|tr[aà]|ô\s*long|o\s*long|olong|ôlong|b[uú]p\s*non|tea\s*365',
        'pc_on_name': 'ASO Tea - Kênh ON (≥12 chai/CH)',
        'pc_on_min_qty': 12,
        'pc_on_channel': 'ON',
        'aso_all_channel': 'OFF',
        'aso_all_name': 'ASO_ALL - Kênh OFF',
        'pc_bt_exclude_meat': False,
        'lppc_moc': 4.0,
        'salary': {
            'TURNOVER': '95%: 4.508.000đ | 100%: 6.440.000đ',
            'PC_BT': '100%: 2.400.000đ (PC=60%×Call, ≥4 line MOQ, trừ Beer)',
            'LPPC': 'Mức 1 (4,0): 2.080.000đ | Mức 2 (4,5): 2.340.000đ | Mức 3 (5,0): 2.600.000đ',
            'ASO_ALL': '100%: 1.100.000đ',
            'ASO_FOCUS': '90%: 880.000đ | 100%: 1.100.000đ (Chanté Active)',
            'ASO_FOCUS_2': '90%: 720.000đ | 100%: 900.000đ (Mì trộn Omachi)',
            'PC_ON': '<30 ASO: 0đ | ≥30 ASO: 1.500.000đ (Tea 365)',
            'LPPC_MEAT': '100%: 400.000đ',
        },
        'holidays': {1, 2},
    },
    'Thang10': {
        'label': 'Tháng 10/2026',
        'year': 2026, 'month': 10,
        'folder': 'Thang10',
        'aso_focus_pat': r'b[uú]p\s*non|bup\s*non|tea\s*365|tea365',
        'aso_focus_name': 'ASO_Focus - Trận Xanh (Tea 365)',
        'aso_focus2_pat': r'homey|hoa tr[aà]\s*jeju|nước giặt xả homey',
        'aso_focus2_name': 'ASO_Focus_2 - Trận Vàng (Homey)',
        'pc_on_pat': r'b[uú]p\s*non|bup\s*non|tea\s*365|tea365',
        'pc_on_name': 'PC_ON - Đơn hàng ≥1 line MOQ (L1 ON)',
        'aso_all_name': 'ASO_ALL - Bao phủ tổng SP Masan (OFF & ON)',
        'pc_bt_exclude_meat': True,
        'lppc_moc': 4.3,
        'salary': {
            'TURNOVER': '95%: 4.508.000đ | 100%: 6.440.000đ',
            'PC_BT': '100%: 2.400.000đ',
            'LPPC': 'Mức 1 (4,3): 1.980.000đ | Mức 2 (4,7): 2.200.000đ',
            'ASO_ALL': '100%: 1.100.000đ',
            'ASO_FOCUS': '90%: 880.000đ | 100%: 1.100.000đ (Tea 365)',
            'ASO_FOCUS_2': '90%: 720.000đ | 100%: 900.000đ (Homey)',
            'PC_ON': '100%: 1.500.000đ',
            'LPPC_MEAT': '100%: 400.000đ',
        },
        'holidays': set(),
    },
}

def get_month_key():
  try:
    return st.session_state.get('report_month_key', 'Thang10')
  except Exception:
    return 'Thang10'

def get_month_cfg():
  return MONTH_OPTIONS.get(get_month_key(), MONTH_OPTIONS['Thang10'])

def get_data_dir():
  """data/Thang09 hoặc data/Thang10; fallback data/ nếu chưa tách."""
  folder = get_month_cfg().get('folder', 'Thang10')
  p = os.path.join('data', folder)
  if os.path.isdir(p):
    return p
  if os.path.isdir('data'):
    return 'data'
  return p

DATA_DIR = 'data'

def _is_sales_filename(fn):
  """True nếu tên file là data chi tiết đơn hàng / RPT (có thể nhiều file/tháng)."""
  if not fn.lower().endswith(('.xlsx', '.xls', '.xlsm')):
    return False
  low = fn.lower().replace(' ', '').replace('_', '').replace('-', '')
  # DanhSachChiTietDonHang.xlsx / (1).xlsx / -2.xlsx / RPT_061...
  return (
      'chitietdonhang' in low
      or 'danhsachchitiet' in low
      or 'rpt061' in low
      or 'lineitem' in low
  )


def _resolve_rpt_paths():
  """Trả về TẤT CẢ file data bán hàng trong thư mục tháng (gộp 2–3 file ≤15 ngày).

  Ví dụ tên file hợp lệ:
    DanhSachChiTietDonHang.xlsx
    DanhSachChiTietDonHang (1).xlsx
    DanhSachChiTietDonHang-2.xlsx
    RPT_061.xlsx
  """
  ddir = get_data_dir()
  found = []
  if os.path.isdir(ddir):
    try:
      for fn in sorted(os.listdir(ddir)):
        if _is_sales_filename(fn):
          found.append(os.path.join(ddir, fn))
    except Exception:
      pass
  if found:
    return found
  # fallback path (có thể chưa tồn tại — caller sẽ báo lỗi)
  return [os.path.join(ddir, 'DanhSachChiTietDonHang.xlsx')]


def _resolve_rpt_path():
  """Giữ API cũ: trả về file đầu tiên (hoặc path mặc định)."""
  paths = _resolve_rpt_paths()
  return paths[0] if paths else os.path.join(get_data_dir(), 'DanhSachChiTietDonHang.xlsx')

def _get_mcp_path():
  return os.path.join(get_data_dir(), 'Data_MCP.xlsx')

def _get_kpi_path():
  return os.path.join(get_data_dir(), 'Target_KPI.xlsx')

def _get_visit_path():
  ddir = get_data_dir()
  for name in ['DanhSachLichViengTham.xlsx', 'DanhSachLichViengTham.xls']:
    p = os.path.join(ddir, name)
    if os.path.isfile(p):
      return p
  return os.path.join(ddir, 'DanhSachLichViengTham.xlsx')

def _get_dskh_trai_path():
  ddir = get_data_dir()
  p = os.path.join(ddir, 'DSKH_Trái Tuyến.xlsx')
  if os.path.isfile(p):
    return p
  if os.path.isdir(ddir):
    for _fn in os.listdir(ddir):
      low = _fn.lower()
      if 'trai' in low.replace('ế', 'e') or 'trái tuyến' in low or 'trai tuyen' in low:
        return os.path.join(ddir, _fn)
  return p

def _list_data_dir():
  ddir = get_data_dir()
  if not os.path.isdir(ddir):
    return []
  try:
    return os.listdir(ddir)
  except Exception:
    return []

def _get_combo_off_path():
  ddir = get_data_dir()
  files = [f for f in _list_data_dir() if 'Combo' in f and 'OFF' in f]
  return os.path.join(ddir, files[0]) if files else os.path.join(ddir, 'Combo Kênh OFF.xlsx')

def _get_combo_on_path():
  ddir = get_data_dir()
  files = [f for f in _list_data_dir() if 'Combo' in f and ('On' in f or 'ON' in f)]
  return os.path.join(ddir, files[0]) if files else os.path.join(ddir, 'Combo Kênh On.xlsx')

def _refresh_paths():
  global RPT_PATH, MCP_PATH, KPI_PATH, VISIT_SCHED_PATH, DSKH_TRAI_PATH
  global COMBO_OFF_PATH, COMBO_ON_PATH, DATA_DIR, CAT_PATH, BRAND_PATH
  DATA_DIR = get_data_dir()
  RPT_PATH = _resolve_rpt_path()
  MCP_PATH = _get_mcp_path()
  KPI_PATH = _get_kpi_path()
  VISIT_SCHED_PATH = _get_visit_path()
  DSKH_TRAI_PATH = _get_dskh_trai_path()
  COMBO_OFF_PATH = _get_combo_off_path()
  COMBO_ON_PATH = _get_combo_on_path()
  CAT_PATH = 'Data_Cat.xlsx'
  BRAND_PATH = 'Data_Brand.xlsx'

# Init paths (an toàn lúc import — chưa có session → Thang10 / data/)
try:
  _refresh_paths()
except Exception:
  RPT_PATH = os.path.join('data', 'DanhSachChiTietDonHang.xlsx')
  MCP_PATH = os.path.join('data', 'Data_MCP.xlsx')
  KPI_PATH = os.path.join('data', 'Target_KPI.xlsx')
  CAT_PATH = 'Data_Cat.xlsx'
  BRAND_PATH = 'Data_Brand.xlsx'
  VISIT_SCHED_PATH = os.path.join('data', 'DanhSachLichViengTham.xlsx')
  DSKH_TRAI_PATH = os.path.join('data', 'DSKH_Trái Tuyến.xlsx')
  COMBO_OFF_PATH = os.path.join('data', 'Combo Kênh OFF.xlsx')
  COMBO_ON_PATH = os.path.join('data', 'Combo Kênh On.xlsx')


# ====================== LOAD ======================
def _read_sales_excel(path):
  """Đọc file chi tiết đơn hàng / RPT — tự tìm dòng header.

  Format mới (DanhSachChiTietDonHang):
    row0 title, row1 date range, row2 blank, row3 = header thật
  Format cũ RPT_061: header ở row 0.
  """
  raw = pd.read_excel(path, header=None, dtype=object)
  header_row = None
  markers = (
      'mã nvbh', 'ma nvbh', 'ngày tạo đơn hàng', 'ngay tao don hang',
      'mã ch', 'ma ch', 'ship-to npp',
  )
  for i in range(min(15, len(raw))):
    vals = [str(x).strip().lower() for x in raw.iloc[i].tolist() if pd.notna(x)]
    joined = ' | '.join(vals)
    if any(m in joined for m in markers) and len(vals) >= 8:
      header_row = i
      break
  if header_row is None:
    header_row = 0
  cols = [
      str(c).strip() if pd.notna(c) else f'Col_{i}'
      for i, c in enumerate(raw.iloc[header_row].tolist())
  ]
  df = raw.iloc[header_row + 1:].copy()
  df.columns = cols
  df = df.dropna(how='all')
  if 'Mã NVBH' in df.columns:
    bad = df['Mã NVBH'].astype(str).str.strip().str.lower()
    df = df[~bad.isin(['mã nvbh', 'ma nvbh', 'nan', ''])]
  return df.reset_index(drop=True)


@st.cache_data(ttl=600)
def load_main_data(_month_key='Thang10'):
  """_month_key: cache riêng theo tháng."""
  try:
    _refresh_paths()
  except Exception:
    pass
  rpt_paths = [p for p in _resolve_rpt_paths() if os.path.isfile(p)]
  if not rpt_paths or not os.path.exists(_get_mcp_path()):
    st.error(
        f"Thiếu file **DanhSachChiTietDonHang*.xlsx** (có thể 1–3 file) "
        f"hoặc **Data_MCP.xlsx** trong thư mục `{DATA_DIR}`"
    )
    st.stop()
  # Gộp tất cả file bán hàng (mỗi file tối đa ~15 ngày)
  _parts = []
  for _p in rpt_paths:
    try:
      _parts.append(_read_sales_excel(_p))
    except Exception as _e:
      st.warning(f'Không đọc được `{os.path.basename(_p)}`: {_e}')
  if not _parts:
    st.error('Không đọc được dữ liệu bán hàng từ các file DanhSachChiTietDonHang*.xlsx')
    st.stop()
  df = pd.concat(_parts, ignore_index=True) if len(_parts) > 1 else _parts[0]
  # Dedup dòng trùng nếu 2 file overlap ngày
  try:
    _dedup_cols = [c for c in [
        'Mã đơn hàng', 'Mã CH', 'Mã sản phẩm', 'Tên sản phẩm',
        'Ngày tạo đơn hàng', 'Tổng tiền', 'Giá trị sau CK',
    ] if c in df.columns]
    if _dedup_cols:
      df = df.drop_duplicates(subset=_dedup_cols, keep='first')
  except Exception:
    pass
  mcp = pd.read_excel(MCP_PATH)

  rename = {}
  for c in df.columns:
    cl = str(c).strip().lower()
    if cl in ('mã ch', 'ma ch', 'outlet code', 'outlet_code') and 'Mã CH' not in df.columns:
      rename[c] = 'Mã CH'
    if (
        cl in ('tên sản phẩm', 'ten san pham', 'product name')
        and 'Tên sản phẩm' not in df.columns
    ):
      rename[c] = 'Tên sản phẩm'
  if rename:
    df = df.rename(columns=rename)

  if 'Tình trạng đơn hàng' in df.columns:
    df = df[df['Tình trạng đơn hàng'].astype(str).str.strip() != 'Đã hủy'].copy()

  if 'Ngày tạo đơn hàng' in df.columns:
    df['Ngày tạo đơn hàng'] = pd.to_datetime(
        df['Ngày tạo đơn hàng'], dayfirst=True, errors='coerce'
    )
    df['date'] = df['Ngày tạo đơn hàng'].dt.date
  else:
    df['date'] = pd.NaT

  c_out = 'Outlet_code' if 'Outlet_code' in mcp.columns else None
  if not c_out:
    for c in mcp.columns:
      if str(c).strip().lower().replace(' ', '_') in ('outlet_code', 'outletcode'):
        c_out = c
        break
  c_l1 = 'L1' if 'L1' in mcp.columns else None
  if c_out and c_l1:
    mcp_map = mcp[[c_out, c_l1]].drop_duplicates(c_out).copy()
    mcp_map[c_out] = mcp_map[c_out].astype(str).str.replace(r'\.0$', '', regex=True)
    mcp_map = mcp_map.rename(columns={c_out: 'Outlet_code', c_l1: 'L1'})
  else:
    mcp_map = pd.DataFrame(columns=['Outlet_code', 'L1'])

  if 'Mã CH' in df.columns:
    df['Mã CH'] = (
        df['Mã CH'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    )
    df = df.merge(mcp_map, left_on='Mã CH', right_on='Outlet_code', how='left')
  if 'Tên sản phẩm' in df.columns:
    df['Tên SP lower'] = df['Tên sản phẩm'].astype(str).str.lower()
  else:
    df['Tên SP lower'] = ''
  return df, mcp


@st.cache_data(ttl=600)
def load_combo_data():
  df_off, df_on = pd.DataFrame(), pd.DataFrame()
  try:
    if os.path.exists(COMBO_OFF_PATH):
      raw_off = pd.read_excel(COMBO_OFF_PATH, header=2)
      new_cols = raw_off.iloc[0].values
      df_off = raw_off.iloc[1:].copy()
      df_off.columns = [
          str(c) if pd.notna(c) else f'Col_{i}'
          for i, c in enumerate(new_cols)
      ]
  except Exception as e:
    print('Error loading Combo OFF:', e)

  try:
    if os.path.exists(COMBO_ON_PATH):
      raw_on = pd.read_excel(COMBO_ON_PATH, header=2)
      new_cols = raw_on.iloc[0].values
      df_on = raw_on.iloc[1:].copy()
      df_on.columns = [
          str(c) if pd.notna(c) else f'Col_{i}'
          for i, c in enumerate(new_cols)
      ]
  except Exception as e:
    print('Error loading Combo ON:', e)

  return df_off, df_on


@st.cache_data(ttl=600)
def load_cat_data():
  for path in [CAT_PATH, os.path.join(get_data_dir(), 'Data_Cat.xlsx')]:
    if os.path.exists(path):
      try:
        return pd.read_excel(path)
      except:
        pass
  return pd.DataFrame()


@st.cache_data(ttl=600)
def load_brand_data():
  for path in [BRAND_PATH, os.path.join(get_data_dir(), 'Data_Brand.xlsx')]:
    if os.path.exists(path):
      try:
        return pd.read_excel(path)
      except:
        pass
  return pd.DataFrame()



@st.cache_data(ttl=600)
def load_visit_schedule():
  """File Danh sách lịch viếng thăm (upload lên data/)."""
  candidates = [
      VISIT_SCHED_PATH,
      os.path.join(get_data_dir(), 'DanhSachLichViengTham.xlsx'),
      os.path.join(get_data_dir(), 'DanhSachLichViengTham.xls'),
      'DanhSachLichViengTham.xlsx',
  ]
  # Tìm file gần đúng tên
  if os.path.isdir(get_data_dir()):
    for f in os.listdir(get_data_dir()):
      fl = f.lower().replace(' ', '')
      if 'lichviengtham' in fl or 'viengtham' in fl or 'danhsachlich' in fl:
        candidates.insert(0, os.path.join(get_data_dir(), f))
  for p in candidates:
    if os.path.exists(p):
      try:
        df = pd.read_excel(p, header=2)
        if 'Ngày lịch VT' in df.columns:
          df['_plan_date'] = pd.to_datetime(
              df['Ngày lịch VT'], dayfirst=True, errors='coerce'
          ).dt.date
        if 'Ngày VT thực tế' in df.columns:
          df['_vt_dt'] = pd.to_datetime(
              df['Ngày VT thực tế'], dayfirst=True, errors='coerce'
          )
        return df
      except Exception as e:
        st.warning(f'Không đọc được file lịch VT ({p}): {e}')
  return pd.DataFrame()


@st.cache_data(ttl=600)
def get_targets():
  if not os.path.exists(_get_kpi_path()):
    return {}
  try:
    kpi = pd.read_excel(_get_kpi_path(), header=None).iloc[2:]
    kpi.columns = [
        'Region',
        'Month',
        'Ship to',
        'Distributor',
        'SUP',
        'SM pos',
        'SM code',
        'SM name',
        'Saleteam',
        'KPI type',
        'KPI Name',
        'Target',
        'Thực hiện',
        '% actual',
        '% Contrib',
        'Chưa ra HĐ',
    ]
    kpi = kpi.dropna(subset=['SM code'])
    kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')
    targets = {}
    for _, r in kpi.iterrows():
      sm, ktype, kname, tgt = (
          str(r['SM code']).strip(),
          str(r['KPI type']).strip(),
          str(r['KPI Name']).strip(),
          r['Target'],
      )
      if pd.isna(tgt):
        continue
      ktype_lower, kname_lower = ktype.lower(), kname.lower()

      if ktype_lower == 'aso_all':
        targets.setdefault(sm, {})['ASO_ALL'] = int(tgt)
      elif ktype_lower == 'pc_bt':
        targets.setdefault(sm, {})['PC_BT'] = int(tgt)
      elif ktype_lower in ('pc_on', 'aso_on'):
        targets.setdefault(sm, {})['PC_ON'] = int(tgt)
      elif ktype_lower == 'lppc' and 'meat' not in kname_lower:
        targets.setdefault(sm, {})['LPPC'] = float(tgt)
      elif ktype_lower in ('lppc_meat', 'lppc meat') or (
          'lppc' in ktype_lower and 'meat' in kname_lower
      ):
        targets.setdefault(sm, {})['LPPC_MEAT'] = float(tgt)
      elif (
          ktype_lower in ('aso_focus', 'aso_focus_1')
          or 'xanh' in kname_lower
          or 'tea 365' in kname_lower
          or 'búp non' in kname_lower
      ):
        targets.setdefault(sm, {})['ASO_FOCUS'] = int(tgt)
      elif (
          ktype_lower == 'aso_focus_2'
          or 'vàng' in kname_lower
          or 'trận vàng' in kname_lower
          or 'homey' in kname_lower
      ):
        targets.setdefault(sm, {})['ASO_FOCUS_2'] = int(tgt)
    return targets
  except:
    return {}


@st.cache_data(ttl=600)
def get_turnover_targets():
  if not os.path.exists(_get_kpi_path()):
    return {}
  try:
    kpi = pd.read_excel(_get_kpi_path(), header=None).iloc[2:]
    kpi.columns = [
        'Region',
        'Month',
        'Ship to',
        'Distributor',
        'SUP',
        'SM pos',
        'SM code',
        'SM name',
        'Saleteam',
        'KPI type',
        'KPI Name',
        'Target',
        'Thực hiện',
        '% actual',
        '% Contrib',
        'Chưa ra HĐ',
    ]
    kpi = kpi.dropna(subset=['SM code'])
    kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')
    targets = {}
    for _, r in kpi.iterrows():
      sm, ktype = str(r['SM code']).strip(), str(r['KPI type']).strip().lower()
      tgt = r['Target']
      if pd.isna(tgt):
        continue
      if ktype == 'turnover':
        targets[sm] = float(tgt)
    return targets
  except:
    return {}


def get_turnover_targets_by_name():
  """Map SM name (normalized) → Target Turnover từ Target_KPI (cùng nguồn báo cáo TURNOVER)."""
  path = _get_kpi_path()
  if not os.path.exists(path):
    return {}
  try:
    kpi = pd.read_excel(path, header=None).iloc[2:]
    kpi.columns = [
        'Region', 'Month', 'Ship to', 'Distributor', 'SUP',
        'SM pos', 'SM code', 'SM name', 'Saleteam',
        'KPI type', 'KPI Name', 'Target', 'Thực hiện',
        '% actual', '% Contrib', 'Chưa ra HĐ',
    ]
    kpi = kpi.dropna(subset=['SM code'])
    kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')
    out = {}
    for _, r in kpi.iterrows():
      ktype = str(r.get('KPI type', '')).strip().lower()
      if ktype != 'turnover':
        continue
      tgt = r['Target']
      if pd.isna(tgt):
        continue
      name = ' '.join(str(r.get('SM name', '')).strip().split())
      if not name or name.lower() in ('nan', 'none'):
        continue
      val = float(tgt)
      prev = float(out.get(name, 0) or 0)
      if val >= prev:
        out[name] = val
        out[name.lower()] = val
    return out
  except Exception:
    return {}


def _scale_row_targets_to_turnover(row, cats, to_tgt):
  """Scale TARGET các ngành của 1 NV để tổng = Target Turnover (đúng)."""
  try:
    to_tgt = float(to_tgt or 0)
  except Exception:
    return row
  if to_tgt <= 0 or not cats:
    return row
  sum_cat = 0.0
  for cat in cats:
    try:
      sum_cat += float(row.get(f'{cat}|TARGET', 0) or 0)
    except Exception:
      pass
  if sum_cat <= 0:
    row['TOTAL|TARGET'] = to_tgt
    so = float(row.get('TOTAL|SELL OUT', 0) or 0)
    row['TOTAL|% MTD'] = round(so / to_tgt * 100, 0) if to_tgt else 0.0
    return row
  ratio = to_tgt / sum_cat
  tot_tg = 0.0
  for cat in cats:
    k = f'{cat}|TARGET'
    try:
      tg = float(row.get(k, 0) or 0) * ratio
    except Exception:
      tg = 0.0
    row[k] = tg
    tot_tg += tg
    so = float(row.get(f'{cat}|SELL OUT', 0) or 0)
    row[f'{cat}|% MTD'] = round(so / tg * 100, 0) if tg > 0 else 0.0
  row['TOTAL|TARGET'] = tot_tg
  so = float(row.get('TOTAL|SELL OUT', 0) or 0)
  row['TOTAL|% MTD'] = round(so / tot_tg * 100, 0) if tot_tg else 0.0
  return row



# Mốc tô màu % theo từng báo cáo Tab KPI
_CURRENT_COLOR_MOC = 100.0
# % Timegone hiện tại của ngày báo cáo; chỉ dùng cho các KPI có lương thưởng.
_CURRENT_TIMEGONE = 100.0
_CURRENT_SALARY_KPI = ''

# KPI có lương thưởng theo Công văn T10/2026 và mốc tối thiểu để được tính lương.
# Khi % KPI đạt mốc tối thiểu này thì được xem là "kịp Timegone" để tô màu.
KPI_SALARY_MIN_PCT = {
    'TURNOVER': 95.0,
    'PC_BT': 100.0,
    'LPPC': 91.5,         # 4.3 / target 4.7 × 100
    'ASO_ALL': 100.0,
    'ASO_FOCUS': 90.0,
    'ASO_FOCUS_2': 90.0,
    'PC_ON': 100.0,
    'LPPC_MEAT': 100.0,
}

# Mốc mặc định (%). LPPC/LPPC_Meat: mốc tuyệt đối (4.3 / 3.8) — xử lý riêng khi set.
KPI_COLOR_MOC = {
    'TURNOVER': 95.0,
    'PC_BT': 100.0,
    'LPPC': 91.5,         # mốc 4.3 / target 4.7 × 100 ≈ 91.5% trên cột % MTD
    'ASO_ALL': 80.0,
    'ASO_FOCUS': 100.0,
    'ASO_FOCUS_2': 100.0,
    'PC_ON': 100.0,
    'LPPC_MEAT': 100.0,   # mốc 3.8 = target → 100% trên cột % MTD
    'COMBO': 100.0,       # sẽ ghi đè bằng % MTD dòng Total khi render
    'SUMMARY': 100.0,
    'MBS_CAT': 100.0,
    'MBS_BRAND': 100.0,
    'VISIT': 100.0,
    'CHANTE': 100.0,
    'OMACHI': 100.0,
    'ASO_TEA': 100.0,
}



@st.cache_data(ttl=600)
def get_all_sm_roster():
  """Danh sách đầy đủ NVBH từ Target_KPI (SM code → SM name).
  Dùng để hiển thị cả NV không có đơn trong RPT (giá trị = 0).
  """
  roster = {}
  if os.path.exists(_get_kpi_path()):
    try:
      kpi = pd.read_excel(_get_kpi_path(), header=None).iloc[2:]
      kpi.columns = [
          'Region', 'Month', 'Ship to', 'Distributor', 'SUP', 'SM pos',
          'SM code', 'SM name', 'Saleteam', 'KPI type', 'KPI Name',
          'Target', 'Thực hiện', '% actual', '% Contrib', 'Chưa ra HĐ',
      ]
      kpi = kpi.dropna(subset=['SM code'])
      for _, r in kpi.iterrows():
        code = str(r['SM code']).strip()
        name = str(r['SM name']).strip() if pd.notna(r['SM name']) else ''
        # Bỏ dòng header / rác
        if code.lower() in ('nan', 'none', '', 'sm code', 'smcode', 'mã nvbh'):
          continue
        if name.lower() in ('sm name', 'sm name', 'tên nvbh', 'nhân viên', 'nan', 'none'):
          name = ''
        _blob = (code + ' ' + name).upper().replace(' ', '').replace('_', '-')
        if 'CDGT-SMVL' in _blob or 'CDGTSMVL' in _blob:
          continue
        if code not in roster or (name and not roster.get(code)):
          roster[code] = name
    except Exception:
      pass
  return roster


def merge_sm_roster(sm_names, all_sms, targets=None, turnover_targets=None, mcp_df=None):
  """Gộp roster Target_KPI + targets + MCP vào sm_names/all_sms."""
  sm_names = dict(sm_names) if sm_names else {}
  all_sms = list(all_sms) if all_sms else []

  roster = get_all_sm_roster()
  for code, name in roster.items():
    if code not in sm_names:
      sm_names[code] = name
    if code not in all_sms:
      all_sms.append(code)

  if targets:
    for code in targets.keys():
      code = str(code).strip()
      if code not in sm_names:
        sm_names[code] = roster.get(code, '')
      if code not in all_sms:
        all_sms.append(code)

  if turnover_targets:
    for code in turnover_targets.keys():
      code = str(code).strip()
      if code not in sm_names:
        sm_names[code] = roster.get(code, '')
      if code not in all_sms:
        all_sms.append(code)

  if mcp_df is not None and not mcp_df.empty:
    c_code = find_col(mcp_df, ['SM Code', 'Mã NVBH', 'SM code'])
    c_name = find_col(mcp_df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    if c_code:
      for _, r in mcp_df[[c_code] + ([c_name] if c_name else [])].drop_duplicates().iterrows():
        code = str(r[c_code]).strip()
        name = str(r[c_name]).strip() if c_name and pd.notna(r.get(c_name)) else roster.get(code, '')
        if code and code.lower() not in ('nan', 'none', ''):
          if code not in sm_names:
            sm_names[code] = name
          if code not in all_sms:
            all_sms.append(code)

  # Xoá tên rác "SM Name" / header
  bad_names = {
      'sm name', 'sm name', 'sm code', 'smcode', 'tên nvbh', 'mã nvbh',
      'nhân viên', 'nan', 'none', '',
  }
  cleaned = {}
  for code, name in sm_names.items():
    code_s = str(code).strip()
    name_s = str(name).strip() if name else ''
    if code_s.lower() in bad_names:
      continue
    if name_s.lower() in bad_names:
      name_s = ''
    # Loại CDGT-SMVL (vị trí ảo)
    _blob = (code_s + ' ' + name_s).upper().replace(' ', '').replace('_', '-')
    if 'CDGT-SMVL' in _blob or 'CDGTSMVL' in _blob:
      continue
    cleaned[code_s] = name_s
  sm_names = cleaned
  all_sms = sorted([c for c in set(all_sms) if str(c).strip().lower() not in bad_names and c in sm_names])
  return sm_names, all_sms



def _is_cdgt_smvl(name_or_code):
  """True nếu là vị trí ảo CDGT-SMVL (không phải NV thật)."""
  s = str(name_or_code or '').upper().replace(' ', '').replace('_', '-')
  return 'CDGT-SMVL' in s or 'CDGTSMVL' in s


def filter_out_cdgt_smvl(df):
  """Loại bỏ dòng CDGT-SMVL khỏi bảng KPI."""
  if df is None or getattr(df, 'empty', True):
    return df
  out = df.copy()
  mask = pd.Series(True, index=out.index)
  for col in ('Tên NVBH', 'Tên NV', 'SM Name', 'Mã NVBH', 'SM code', 'SM Code'):
    if col in out.columns:
      mask = mask & ~out[col].astype(str).map(_is_cdgt_smvl)
  out = out[mask].copy()
  if out.empty:
    return out.reset_index(drop=True)
  if 'STT' in out.columns:
    name_s = out['Tên NVBH'].astype(str) if 'Tên NVBH' in out.columns else pd.Series('', index=out.index)
    is_tot = out['STT'].astype(str).str.strip().isin(['-', '—']) | name_s.str.contains(
        'Total|TỔNG', case=False, na=False
    )
    body = out[~is_tot].copy()
    tot = out[is_tot].copy()
    if not body.empty:
      body = body.reset_index(drop=True)
      body['STT'] = range(1, len(body) + 1)
    out = pd.concat([body, tot], ignore_index=True)
  return out.reset_index(drop=True)


def set_color_moc(moc):
  global _CURRENT_COLOR_MOC
  try:
    _CURRENT_COLOR_MOC = float(moc)
  except Exception:
    _CURRENT_COLOR_MOC = 100.0


def set_timegone_color_context(pct_timegone):
  """Cập nhật % Timegone của ngày báo cáo để tô màu KPI có lương thưởng."""
  global _CURRENT_TIMEGONE
  try:
    _CURRENT_TIMEGONE = float(pct_timegone)
  except Exception:
    _CURRENT_TIMEGONE = 100.0


def set_color_moc_for_kpi(kpi_key, total_pct=None):
  """
  Gán mốc tô màu theo loại báo cáo.
  Với 8 KPI có lương thưởng: màu % bám theo Timegone; đồng thời
  nếu đạt mốc tối thiểu tính lương thì được xem như đã kịp Timegone.
  Riêng LPPC/LPPC_Meat, bảng sẽ có thêm màu theo đúng mốc lương tuyệt đối.
  Combo: dùng % MTD dòng Total nếu có.
  """
  global _CURRENT_SALARY_KPI
  _CURRENT_SALARY_KPI = str(kpi_key)
  if kpi_key == 'COMBO' and total_pct is not None:
    set_color_moc(total_pct)
    return

  kpi_key = str(kpi_key)
  if kpi_key in KPI_SALARY_MIN_PCT:
    # OR logic: đạt Timegone HOẶC đạt mốc tối thiểu tính lương => được xem là kịp.
    # Dùng mốc thấp hơn để vùng xanh bắt đầu từ ngưỡng sớm hơn trong hai điều kiện.
    effective_moc = min(
        float(_CURRENT_TIMEGONE),
        float(KPI_SALARY_MIN_PCT[kpi_key]),
    )
    set_color_moc(effective_moc)
    return

  moc = KPI_COLOR_MOC.get(kpi_key, 100.0)
  set_color_moc(moc)


def color_pct_bg(val, moc=None):
  """Tô màu theo mốc báo cáo (inline style)."""
  try:
    v = float(str(val).replace('%', '').strip())
    p = float(moc) if moc is not None else float(_CURRENT_COLOR_MOC)
    if v < p:
      return (
          'background-color:#fed7d7 !important;color:#742a2a !important;'
          'font-weight:700 !important;'
      )
    elif v <= p + 5:
      return (
          'background-color:#c6f6d5 !important;color:#22543d !important;'
          'font-weight:700 !important;'
      )
    else:
      return (
          'background-color:#e9d8fd !important;color:#553c9a !important;'
          'font-weight:700 !important;'
      )
  except Exception:
    return ''


def color_pct_class(val, moc=None):
  """Class CSS cho cột % (tránh bị zebra đè)."""
  try:
    v = float(str(val).replace('%', '').strip())
    p = float(moc) if moc is not None else float(_CURRENT_COLOR_MOC)
    if v < p:
      return 'pct-red'
    elif v <= p + 5:
      return 'pct-green'
    else:
      return 'pct-purple'
  except Exception:
    return ''


def salary_metric_style(kpi_key, col, val):
  """Chỉ tô màu cột % MTD cho LPPC / LPPC_Meat.

  LPPC % MTD: <91.5 đỏ; 91.5–<100 xanh; >=100 tím.
  LPPC_Meat % MTD: <100 đỏ; =100 xanh; >100 tím.
  Cột Thực Hiện Ngày / MTD: KHÔNG tô màu.
  """
  key = str(kpi_key or '').upper()
  c = str(col or '').strip().upper()
  try:
    v = float(str(val).replace('%', '').replace(',', '').strip())
  except Exception:
    return '', ''

  red = 'background-color:#fed7d7 !important;color:#742a2a !important;font-weight:800 !important;'
  green = 'background-color:#c6f6d5 !important;color:#22543d !important;font-weight:800 !important;'
  purple = 'background-color:#e9d8fd !important;color:#553c9a !important;font-weight:800 !important;'

  # Chỉ áp dụng cho cột %
  if '%' not in c:
    return '', ''

  if key == 'LPPC':
    if v < 91.5:
      return 'pct-red', red
    if v < 100:
      return 'pct-green', green
    return 'pct-purple', purple

  if key == 'LPPC_MEAT':
    if v < 100:
      return 'pct-red', red
    if v == 100:
      return 'pct-green', green
    return 'pct-purple', purple

  return '', ''



def vip_ko_bg(val):
  """VIP KO ĐH: từ 1 tô đỏ, số càng lớn càng đỏ đậm."""
  try:
    v = int(float(str(val).strip()))
  except Exception:
    return ''
  if v <= 0:
    return ''
  if v <= 2:
    return (
        'background-color:#fed7d7 !important;color:#742a2a !important;'
        'font-weight:700 !important;'
    )
  if v <= 5:
    return (
        'background-color:#feb2b2 !important;color:#822727 !important;'
        'font-weight:700 !important;'
    )
  if v <= 9:
    return (
        'background-color:#fc8181 !important;color:#742a2a !important;'
        'font-weight:800 !important;'
    )
  return (
      'background-color:#c53030 !important;color:#ffffff !important;'
      'font-weight:900 !important;'
  )


def vip_ko_class(val):
  try:
    v = int(float(str(val).strip()))
  except Exception:
    return ''
  if v <= 0:
    return ''
  if v <= 2:
    return 'vip-1'
  if v <= 5:
    return 'vip-2'
  if v <= 9:
    return 'vip-3'
  return 'vip-4'


def format_number_vn(x):
  try:
    if pd.isnull(x) or str(x).lower() in ['none', 'nan', '']:
      return ''
    return f'{float(x):,.0f}'.replace(',', '.')
  except:
    return x


def format_scaled_thousand(x):
  try:
    if pd.isnull(x) or str(x).lower() in ['none', 'nan', '']:
      return ''
    val = float(x) / 1000.0
    return f'{val:,.0f}'.replace(',', '.')
  except:
    return x


def find_col(df, candidates):
  cols = {c.lower().strip(): c for c in df.columns}
  for c in candidates:
    if c.lower() in cols:
      return cols[c.lower()]
  return None



def nv_selected(filter_nv):
  """True nếu đang lọc NV cụ thể (list/str không rỗng, không phải Tất cả)."""
  if filter_nv is None:
    return False
  if isinstance(filter_nv, list):
    return len(filter_nv) > 0 and 'Tất cả ĐDKD' not in filter_nv
  return str(filter_nv).strip() not in ('', 'Tất cả ĐDKD')


def nv_label(filter_nv):
  if not nv_selected(filter_nv):
    return 'Tất cả ĐDKD'
  if isinstance(filter_nv, list):
    return ', '.join(str(x) for x in filter_nv)
  return str(filter_nv)


def filter_df_by_nv(df, col, filter_nv):
  """Lọc DataFrame theo cột NV; hỗ trợ list (multi) hoặc str."""
  if df is None or df.empty or not col or col not in df.columns:
    return df
  if not nv_selected(filter_nv):
    return df
  vals = filter_nv if isinstance(filter_nv, list) else [filter_nv]
  return df[df[col].astype(str).str.strip().isin([str(v).strip() for v in vals])]



def filter_by_thu_multi(df, col_thu, f_thu_list):
  if not f_thu_list or not col_thu:
    return df
  thu_s = df[col_thu].astype(str).str.strip()
  mask = pd.Series(False, index=df.index)

  mapping_rules = {
      '2': ['2', '25'],
      '3': ['3', '36'],
      '4': ['4', '47'],
      '5': ['5', '25'],
      '6': ['6', '36'],
      '7': ['7', '47'],
      '25': ['25'],
      '36': ['36'],
      '47': ['47'],
  }

  for f_thu in f_thu_list:
    valid_set = mapping_rules.get(str(f_thu).strip(), [str(f_thu).strip()])
    mask = mask | thu_s.isin(valid_set)
  return df[mask]


def filter_by_odd_week(df, report_date):
  """Lọc cửa hàng theo tuần chẵn/lẻ ISO dựa trên cột ODD_WEEK.
  - Tuần lẻ (ISO week % 2 == 1): giữ Odd Week + Both
  - Tuần chẵn (ISO week % 2 == 0): giữ Even Week + Both
  """
  if df is None or df.empty or report_date is None:
    return df

  # Tìm cột ODD_WEEK (nhiều biến thể tên)
  col = find_col(df, ['ODD_WEEK', 'Odd_Week', 'Odd Week', 'WEEK_TYPE', 'Week Type'])
  if not col:
    for c in df.columns:
      cl = str(c).lower().replace(' ', '').replace('_', '')
      if 'oddweek' in cl or (cl == 'oddweek') or ('odd' in cl and 'week' in cl):
        col = c
        break
  if not col:
    return df

  iso_week = int(report_date.isocalendar()[1])
  is_odd_week = (iso_week % 2 == 1)  # 1,3,5... = Tuần Lẻ

  # Chuẩn hoá giá trị
  raw = df[col]
  s = (
      raw.astype(str)
      .str.strip()
      .str.lower()
      .str.replace('_', ' ', regex=False)
      .str.replace(r'\s+', ' ', regex=True)
  )

  both_mask = (
      s.isin(['both', 'cả hai', 'ca hai', 'all', 'nan', 'none', '', 'nat'])
      | raw.isna()
  )
  odd_mask = s.isin(['odd week', 'odd', 'tuần lẻ', 'tuan le', 'lẻ', 'le'])
  even_mask = s.isin(['even week', 'even', 'tuần chẵn', 'tuan chan', 'chẵn', 'chan'])

  if is_odd_week:
    keep = both_mask | odd_mask
  else:
    keep = both_mask | even_mask

  return df.loc[keep].copy()


def process_mcp_sales(df_rpt, df_mcp):
  if df_mcp.empty or df_rpt.empty:
    return df_mcp
  valid_df = df_rpt[df_rpt['Tình trạng đơn hàng'] != 'Đã hủy'].copy()
  val_col = (
      find_col(valid_df, ['Tổng tiền', 'Giá trị sau CK', 'Doanh thu'])
      or 'Tổng tiền'
  )
  valid_df['Mã CH_str'] = valid_df['Mã CH'].astype(str).str.strip()
  sales_agg = valid_df.groupby('Mã CH_str')[val_col].sum().reset_index()
  sales_agg.columns = ['Outlet_code_key', 'Total_Sales']

  df_out = df_mcp.copy()
  code_col = find_col(df_out, ['Outlet_code', 'Outlet Code', 'Mã CH'])
  sales_col = find_col(df_out, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])

  if not code_col:
    return df_out
  df_out['_key'] = df_out[code_col].astype(str).str.strip()
  sales_agg['Outlet_code_key'] = sales_agg['Outlet_code_key'].astype(str)
  df_out = df_out.merge(
      sales_agg, left_on='_key', right_on='Outlet_code_key', how='left'
  )

  target_sales_col = sales_col if sales_col else 'Doanh Số MTD'
  df_out[target_sales_col] = df_out['Total_Sales'].fillna(0.0)

  drop_cols = [
      c
      for c in ['_key', 'Outlet_code_key', 'Total_Sales']
      if c in df_out.columns
  ]
  return df_out.drop(columns=drop_cols)


def build_mcp_sales_detail(df_rpt, df_mcp, report_date=None):
  """Giữ NGUYÊN mọi cột Data_MCP + thêm Sub Division, Group STD SKU, Tên sản phẩm, Doanh Số MTD chi tiết."""
  if df_mcp is None or df_mcp.empty:
    return pd.DataFrame()

  mcp = df_mcp.copy()
  c_ma = find_col(
      mcp,
      ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã khách hàng', 'Poscode', 'outlet_code'],
  )
  if not c_ma:
    return mcp

  mcp = mcp.copy()
  mcp['__ma'] = mcp[c_ma].astype(str).str.strip()
  mcp['__ma'] = mcp['__ma'].map(
      lambda x: x[:-2] if isinstance(x, str) and x.endswith('.0') else x
  )

  detail = pd.DataFrame(columns=['__ma', 'Sub Division', 'Group STD SKU', 'Tên sản phẩm', '__ds'])
  if df_rpt is not None and not df_rpt.empty:
    d = df_rpt.copy()
    status = find_col(d, ['Tình trạng đơn hàng', 'Trạng thái'])
    if status:
      d = d[~d[status].astype(str).str.contains('hủy|cancel', case=False, na=False)]
    if report_date is not None and 'date' in d.columns:
      try:
        rd = report_date if isinstance(report_date, date) else pd.Timestamp(report_date).date()
        start = date(rd.year, rd.month, 1)
        d = d[(d['date'] >= start) & (d['date'] <= rd)]
      except Exception:
        pass
    c_ch = find_col(d, ['Mã CH', 'Outlet_code', 'Outlet Code'])
    c_sub = find_col(d, ['Sub Division', 'SubDivision', 'Phân nhóm', 'SUB DIV'])
    c_grp = find_col(
        d,
        ['Group STD', 'Group std', 'Group STD SKU', 'GROUP_STD', 'Standard Group', 'STD Group', 'Nhóm STD'],
    )
    c_sp = find_col(
        d,
        ['Tên sản phẩm', 'Tên SP', 'Item name', 'Product name', 'STANDARD_SKU_NAME'],
    )
    c_val = find_col(d, ['Tổng tiền', 'Giá trị sau CK', 'Doanh thu']) or 'Tổng tiền'
    if c_ch and c_val in d.columns:
      d['__ma'] = d[c_ch].astype(str).str.strip()
      d['__ma'] = d['__ma'].map(
          lambda x: x[:-2] if isinstance(x, str) and x.endswith('.0') else x
      )
      d['__sub'] = d[c_sub].astype(str).str.strip() if c_sub else ''
      d['__grp'] = d[c_grp].astype(str).str.strip() if c_grp else ''
      d['__sp'] = d[c_sp].astype(str).str.strip() if c_sp else ''
      d['__val'] = pd.to_numeric(d[c_val], errors='coerce').fillna(0)
      for col in ('__sub', '__grp', '__sp'):
        d[col] = d[col].replace({'nan': '', 'None': '', 'NaN': ''})
      detail = (
          d.groupby(['__ma', '__sub', '__grp', '__sp'], dropna=False)['__val']
          .sum()
          .reset_index()
      )
      detail.columns = ['__ma', 'Sub Division', 'Group STD SKU', 'Tên sản phẩm', '__ds']

  # FULL MCP rows (không cắt cột)
  mcp_base = mcp.drop_duplicates(subset=['__ma'], keep='first')

  if detail.empty:
    out = mcp_base.copy()
    out['Sub Division'] = ''
    out['Group STD SKU'] = ''
    out['Tên sản phẩm'] = ''
    ds_col = find_col(out, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])
    if ds_col:
      out[ds_col] = 0.0
    else:
      out['Doanh Số MTD'] = 0.0
    return out.drop(columns=['__ma'], errors='ignore')

  out = mcp_base.merge(detail, on='__ma', how='left')
  out['Sub Division'] = out['Sub Division'].fillna('')
  out['Group STD SKU'] = out['Group STD SKU'].fillna('')
  out['Tên sản phẩm'] = out['Tên sản phẩm'].fillna('')
  out['__ds'] = pd.to_numeric(out['__ds'], errors='coerce').fillna(0.0)

  ds_col = find_col(out, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])
  if ds_col:
    out[ds_col] = out['__ds']
  else:
    out['Doanh Số MTD'] = out['__ds']

  out = out.drop(columns=['__ma', '__ds'], errors='ignore')

  c_nv = find_col(out, ['SM name', 'SM Name', 'Tên NVBH', 'Nhân viên'])
  sort_cols = []
  if c_nv:
    sort_cols.append(c_nv)
  sort_cols.append(c_ma)
  ds_final = find_col(out, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])
  if ds_final:
    sort_cols.append(ds_final)
  if sort_cols:
    ascending = [c != ds_final for c in sort_cols]
    try:
      out = out.sort_values(sort_cols, ascending=ascending).reset_index(drop=True)
    except Exception:
      pass
  return out




def build_mcp_nv_summary(
    df_mcp,
    df_detail_filtered,
    filter_nv=None,
    f_sub=None,
    f_grp=None,
    f_sp=None,
    report_date=None,
    df_perf_raw=None,
    df_rpt=None,
):
  """Tổng hợp theo NV.

  Chỉ tiêu (TARGETACTUAL):
    Sub Division  → SUB DIV
    Group STD SKU → KPI_OBJ_CATLOG (đúng tên group; fallback BRAND nếu không khớp)
    Tên sản phẩm  → STANDARD_SKU_DESC_2 (fuzzy) / STANDARD_SKU_CODE

  MTD: Thành tiền trước CK từ RPT, lọc cùng Sub/Group/SP.
  """
  cols = [
      'STT', 'Tên NVBH', 'Chỉ tiêu Doanh Số', 'MTD', '% MTD DS',
      'MCP', 'ASO', '% MTD ASO/MCP',
  ]
  empty = pd.DataFrame(columns=cols)
  if df_mcp is None or df_mcp.empty:
    return empty

  def _norm(x):
    s = str(x).strip()
    return s[:-2] if s.endswith('.0') else s

  def _norm_key(x):
    return str(x).strip().lower()

  def _norm_nv(x):
    return re.sub(r'\s+', ' ', str(x).strip())

  def _tokens(s):
    s = _norm_key(s)
    s = re.sub(r'^\d{3,5}\s*[-–:]\s*', '', s)
    s = re.sub(
        r'\b(\d+\s*[x×]\s*)+(\d+\s*)?(bl|chai|hộp|goi|gói|lon|thùng|loc|lốc)?\b',
        ' ', s, flags=re.I,
    )
    s = re.sub(r'\b\d+([.,]\d+)?\s*(ml|gr|g|kg|l|lit|mm)\b', ' ', s, flags=re.I)
    s = re.sub(
        r'[^a-z0-9àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ\s]',
        ' ', s,
    )
    stop = {
        'x', 'bl', 'chai', 'hop', 'hộp', 'goi', 'gói', 'lon', 'thung', 'thùng',
        'loc', 'lốc', 'ml', 'gr', 'kg', 'va', 'và', 'cua', 'của',
    }
    return {t for t in s.split() if t and t not in stop and len(t) > 1}

  def _fuzzy_product(cell_val, filter_vals, min_ratio=0.8):
    """Match SP: ưu tiên exact/contains; fuzzy yêu cầu ≥80% token filter nằm trong cell.
    Loại biến thể (amazon, …) nếu filter không chứa token đó.
    """
    if cell_val is None or (isinstance(cell_val, float) and pd.isna(cell_val)):
      return False
    cell = str(cell_val).strip()
    if not cell or cell.lower() in ('nan', 'none'):
      return False
    cl = cell.lower()
    cl2 = re.sub(r'^\d{3,5}\s*[-–:]\s*', '', cl).strip()
    ct = _tokens(cell)
    # token đặc trưng của biến thể — chỉ chấp nhận nếu filter cũng có
    variant_tokens = {
        'amazon', 'compact', 'lemona', 'vivant', 'chanh', 'cam', 'dâu', 'dau',
        'xoài', 'xoai', 'vải', 'vai', 'đào', 'dao',
    }
    for fv in filter_vals:
      fl = _norm_key(fv)
      if not fl:
        continue
      if cl == fl or cl2 == fl:
        return True
      # contains: filter nằm gọn trong cell (sau bỏ mã) hoặc ngược lại nếu cell ngắn
      if fl in cl2 or fl in cl:
        return True
      if len(cl2) >= 10 and cl2 in fl:
        return True
      ft = _tokens(fv)
      if not ct or not ft:
        continue
      # loại biến thể không có trong filter
      extra_var = (ct & variant_tokens) - ft
      if extra_var:
        continue
      inter = ct & ft
      # phần lớn token của FILTER phải có trong cell
      cover = len(inter) / len(ft)
      if cover >= min_ratio and len(inter) >= 3:
        return True
    return False

  def _match_group_series(series, filter_vals):
    """Exact → contains full string → fuzzy token (min 3 token chung)."""
    s = series.astype(str).str.strip()
    low = s.str.lower()
    f_low = [_norm_key(x) for x in filter_vals if str(x).strip()]
    mask = pd.Series(False, index=series.index)
    for fl in f_low:
      mask = mask | (low == fl)
    if not mask.any():
      for fl in f_low:
        if len(fl) >= 4:
          mask = mask | low.str.contains(re.escape(fl), na=False)
    if not mask.any():
      # fuzzy nhẹ: cần ≥ 3 token chung
      def _ok(v):
        vt = _tokens(v)
        for fl in f_low:
          ft = _tokens(fl)
          if not vt or not ft:
            continue
          inter = vt & ft
          if len(inter) >= 3 and len(inter) / min(len(vt), len(ft)) >= 0.6:
            return True
        return False
      mask = s.apply(_ok)
    return mask

  mcp = df_mcp.copy()
  c_nv = find_col(mcp, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
  c_ma = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH'])
  if not c_nv or not c_ma:
    return empty

  mcp['_nv'] = mcp[c_nv].map(_norm_nv)
  mcp['_ma'] = mcp[c_ma].map(_norm)
  if filter_nv:
    if isinstance(filter_nv, (list, tuple, set)):
      allow = {_norm_nv(x) for x in filter_nv}
      mcp = mcp[mcp['_nv'].isin(allow)]
    else:
      mcp = mcp[mcp['_nv'] == _norm_nv(filter_nv)]

  mcp_cnt = mcp.groupby('_nv')['_ma'].nunique().to_dict()

  # ----- ASO -----
  aso_map = {}
  detail = df_detail_filtered.copy() if df_detail_filtered is not None else pd.DataFrame()
  if not detail.empty:
    d_nv = find_col(detail, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    d_ma = find_col(detail, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH'])
    d_ds = find_col(detail, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])
    if d_nv and d_ds and d_ma:
      detail['_nv'] = detail[d_nv].map(_norm_nv)
      detail['_ma'] = detail[d_ma].map(_norm)
      detail['_ds'] = pd.to_numeric(detail[d_ds], errors='coerce').fillna(0)
      aso_map = (
          detail[detail['_ds'] > 0]
          .groupby('_nv')['_ma']
          .nunique()
          .to_dict()
      )

  # ----- MTD từ RPT -----
  mtd_map = {}
  mtd_full_map = {}
  if df_rpt is not None and not getattr(df_rpt, 'empty', True) and report_date is not None:
    d = df_rpt.copy()
    if 'date' in d.columns:
      d['_d'] = pd.to_datetime(d['date'], errors='coerce')
    else:
      c_date = find_col(d, [
          'Ngày tạo đơn hàng', 'Ngày tạo đơn', 'Order Date', 'ORDER_DT',
      ])
      d['_d'] = (
          pd.to_datetime(d[c_date], dayfirst=True, errors='coerce')
          if c_date else pd.NaT
      )

    c_cat = find_col(d, ['Sub Division', 'SUB DIV', 'SubDivision', 'Phân nhóm'])
    c_grp = find_col(
        d,
        ['Group STD', 'Group std', 'Group STD SKU', 'GROUP_STD', 'Standard Group', 'STD Group', 'Nhóm STD'],
    )
    c_sp = find_col(
        d,
        ['Tên sản phẩm', 'Tên SP', 'Item name', 'Product name', 'STANDARD_SKU_NAME', 'STANDARD_SKU_DESC_2'],
    )
    c_nv_r = find_col(d, ['Tên NVBH', 'SM NAME', 'SM_NAME', 'Nhân viên'])
    c_val = find_col(d, [
        'Thành tiền trước CK', 'Thành tiền trước chiết khấu',
        'Tổng tiền', 'Giá trị sau CK', 'Doanh thu',
    ])
    c_status = find_col(d, ['Tình trạng đơn hàng', 'Status', 'STATUS_CD'])

    if c_val is not None:
      y, m = int(report_date.year), int(report_date.month)
      d = d[d['_d'].apply(
          lambda x: (int(x.year), int(x.month)) == (y, m) if pd.notna(x) else False
      )]
      if c_status:
        st = d[c_status].astype(str).str.strip().str.lower()
        d = d[~st.isin(['đã hủy', 'da huy', 'cancelled', 'canceled'])]
        d = d[~st.str.contains('hủy|huy', na=False)]

      if f_sub and c_cat:
        low = {_norm_key(x) for x in f_sub}
        d = d[d[c_cat].astype(str).str.strip().str.lower().isin(low)]
      if f_grp and c_grp:
        d = d[_match_group_series(d[c_grp], f_grp)]
      if f_sp and c_sp:
        low = {_norm_key(x) for x in f_sp}
        mask = d[c_sp].astype(str).str.strip().str.lower().isin(low)
        if not mask.any():
          mask = d[c_sp].apply(lambda v: _fuzzy_product(v, f_sp))
        d = d[mask]

      d['_val'] = pd.to_numeric(d[c_val], errors='coerce').fillna(0)
      if c_nv_r:
        d['_nv'] = d[c_nv_r].map(_norm_nv)
        if filter_nv:
          if isinstance(filter_nv, (list, tuple, set)):
            d = d[d['_nv'].isin({_norm_nv(x) for x in filter_nv})]
          else:
            d = d[d['_nv'] == _norm_nv(filter_nv)]
        mtd_full_map = d.groupby('_nv')['_val'].sum().to_dict()
        # Lọc MTD theo CH đang chọn (VIP/L1/…)
        c_ma_r = find_col(d, ['Mã CH', 'Mã KH', 'Outlet_code', 'Outlet Code'])
        if c_ma_r is not None and '_ma' in mcp.columns:
          allow_ma = set(mcp['_ma'].astype(str).tolist())
          d = d.copy()
          d['_ma_r'] = d[c_ma_r].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
          d = d[d['_ma_r'].isin(allow_ma)]
        mtd_map = d.groupby('_nv')['_val'].sum().to_dict() if not d.empty else {}

  # ----- Chỉ tiêu từ Performance -----
  target_map = {}
  try:
    perf = df_perf_raw if df_perf_raw is not None else load_perf_sku_data()
  except Exception:
    perf = pd.DataFrame()

  if perf is not None and not getattr(perf, 'empty', True):
    p = perf.copy()
    p.columns = [re.sub(r"^['\"]|['\"]$", '', str(c)).strip() for c in p.columns]

    c_month = find_col(p, ['MONTH', 'Month'])
    c_cat = find_col(p, ['SUB DIV', 'SUB_DIV', 'Sub Division', 'CAT', 'Category'])
    c_grp_p = find_col(p, [
        'KPI_OBJ_CATLOG', 'KPI OBJ CATLOG', 'KPI_OBJ_CATALOG',
        'Group STD', 'Group STD SKU', 'GROUP_STD',
    ])
    c_brand_p = find_col(p, ['BRAND', 'Brand', 'Nhãn', 'Nhãn hàng'])
    c_sp_p = find_col(p, [
        'STANDARD_SKU_DESC_2', 'STANDARD_SKU_DESC', 'STANDARD_SKU_NAME',
        'Tên sản phẩm', 'Tên SP', 'SKU NAME',
    ])
    c_sku_code = find_col(p, ['STANDARD_SKU_CODE', 'STD_SKU_CODE', 'SKU_CODE'])
    c_tg = find_col(p, ['TARGET SO', 'Target SO', 'TARGET', 'Target'])
    c_pnv = find_col(p, ['SM NAME', 'SM_NAME', 'Tên NVBH', 'SM name'])

    if c_month and c_tg and c_pnv:
      cur_m = _month_key_from_date(report_date) if report_date is not None else ''
      p['_month'] = p[c_month].astype(str).str.strip()
      if cur_m:
        p = p[p['_month'] == cur_m]
      p['_nv'] = p[c_pnv].map(_norm_nv)
      p['_tg'] = pd.to_numeric(p[c_tg], errors='coerce').fillna(0)

      # 1) Sub Division
      if f_sub and c_cat:
        low = {_norm_key(x) for x in f_sub}
        p = p[p[c_cat].astype(str).str.strip().str.lower().isin(low)]

      # 2) Group STD SKU → KPI_OBJ_CATLOG (không OR BRAND ngay)
      if f_grp and c_grp_p:
        mask = _match_group_series(p[c_grp_p], f_grp)
        if not mask.any() and c_brand_p is not None:
          # fallback BRAND chỉ khi KPI không khớp
          mask = _match_group_series(p[c_brand_p], f_grp)
        p = p[mask]

      # 3) Tên SP → STANDARD_SKU_DESC_2 (best-match từng tên lọc)
      if f_sp and c_sp_p:
        def _core_name(s):
          s = str(s).lower().strip()
          s = re.sub(r'^\d{3,5}\s*[-–:]\s*', '', s)
          s = re.sub(r'\d+([.,]\d+)?', ' ', s)
          s = re.sub(
              r'\b(bl|chai|hop|hộp|goi|gói|lon|thung|thùng|loc|lốc|ml|gr|kg|x)\b',
              ' ', s,
          )
          s = re.sub(
              r'[^a-z0-9àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ\s]',
              ' ', s,
          )
          return re.sub(r'\s+', ' ', s).strip()

        def _score_sp(filter_name, perf_desc):
          a = _core_name(filter_name)
          b = _core_name(perf_desc)
          if not a or not b:
            return 0.0
          if a == b:
            return 1.0
          if a in b or b in a:
            return 0.95
          ta, tb = set(a.split()), set(b.split())
          if not ta or not tb:
            return 0.0
          inter = ta & tb
          cover_f = len(inter) / len(ta)
          cover_p = len(inter) / len(tb)
          variants = {'amazon', 'compact', 'lemona', 'vivant'}
          if (tb & variants) - ta:
            return 0.0
          # token set gần giống (bỏ qua thứ tự)
          if ta == tb:
            return 0.98
          if cover_f >= 0.85 and len(inter) >= 3:
            return 0.9 + 0.08 * cover_f
          seq = difflib.SequenceMatcher(None, a, b).ratio()
          return max(seq * cover_f, cover_f * 0.85)

        perf_descs = (
            p[c_sp_p].dropna().astype(str).map(lambda x: x.strip()).unique().tolist()
        )
        matched = set()
        for fv in f_sp:
          scored = []
          for desc in perf_descs:
            sc = _score_sp(fv, desc)
            if sc >= 0.65:
              scored.append((sc, desc))
          if not scored:
            continue
          scored.sort(reverse=True)
          best_sc = scored[0][0]
          for sc, desc in scored:
            # lấy best + các desc gần best
            if sc >= best_sc - 0.05 or sc >= 0.85:
              matched.add(desc)

        if matched:
          p = p[p[c_sp_p].astype(str).str.strip().isin(matched)]
        else:
          mask = p[c_sp_p].apply(lambda v: _fuzzy_product(v, f_sp))
          if (not isinstance(mask, pd.Series) or not mask.any()) and c_sku_code is not None:
            codes = set()
            for s in f_sp:
              m = re.match(r'^(\d{3,5})\b', str(s).strip())
              if m:
                codes.add(m.group(1))
            # cũng lấy code từ STANDARD_SKU_DESC_2 nếu core name khớp mạnh
            if not codes:
              for desc in perf_descs:
                if _score_sp(f_sp[0], desc) >= 0.65:
                  m = re.match(r'^(\d{3,5})\b', str(desc).strip())
                  if m:
                    codes.add(m.group(1))
            if codes:
              mask = p[c_sku_code].astype(str).str.strip().isin(codes)
          if isinstance(mask, pd.Series) and mask.any():
            p = p[mask]
          else:
            p = p.iloc[0:0]

      if filter_nv:
        if isinstance(filter_nv, (list, tuple, set)):
          p = p[p['_nv'].isin({_norm_nv(x) for x in filter_nv})]
        else:
          p = p[p['_nv'] == _norm_nv(filter_nv)]

      target_map = p.groupby('_nv')['_tg'].sum().to_dict()

  nvs = sorted(set(list(mcp_cnt.keys()) + list(mtd_map.keys()) + list(target_map.keys())))
  if filter_nv:
    if isinstance(filter_nv, (list, tuple, set)):
      allow = {_norm_nv(x) for x in filter_nv}
      nvs = [n for n in nvs if n in allow]
    else:
      nvs = [n for n in nvs if n == _norm_nv(filter_nv)]

  rows = []
  for nv in nvs:
    ct = float(target_map.get(nv, 0) or 0)
    mtd = float(mtd_map.get(nv, 0) or 0)
    mtd_full = float(mtd_full_map.get(nv, 0) or 0)
    # Khi lọc nhóm KH (VIP/L1/…): scale chỉ tiêu theo tỷ trọng MTD nhóm / MTD full
    if mtd_full > 0 and abs(mtd_full - mtd) > 1:
      ct = ct * (mtd / mtd_full)
    elif mtd_full > 0 and mtd == 0:
      ct = 0.0
    pct_ds = round(mtd / ct * 100, 1) if ct > 0 else 0.0
    mcp_n = int(mcp_cnt.get(nv, 0) or 0)
    aso_n = int(aso_map.get(nv, 0) or 0)
    pct_aso = round(aso_n / mcp_n * 100, 1) if mcp_n > 0 else 0.0
    rows.append({
        'Tên NVBH': nv,
        'Chỉ tiêu Doanh Số': round(ct, 0),
        'MTD': mtd,
        '% MTD DS': pct_ds,
        'MCP': mcp_n,
        'ASO': aso_n,
        '% MTD ASO/MCP': pct_aso,
    })

  out = pd.DataFrame(rows)
  if out.empty:
    return empty
  out = out.sort_values('Tên NVBH').reset_index(drop=True)
  out.insert(0, 'STT', range(1, len(out) + 1))
  return out[cols]



def process_cat_sales(df_rpt, df_cat):
  if df_cat.empty or df_rpt.empty:
    return df_cat
  sub_map = {
      'Beer': 'Bia',
      'Coffee': 'Cà phê',
      'Seasoning': 'Gia vị',
      'Home Care': 'Hóa Mỹ Phẩm',
      'Convenience Foods': 'Mì, Lẩu, Phở, Hủ Tiếu',
      'Refreshment Drinks': 'Nước giải khát',
      'Nutrition': 'Ngũ cốc',
      'Processed Meats': 'Xúc xích, Thịt chế biến',
  }
  df_clean = df_rpt.copy()
  sub_div_col = find_col(df_clean, ['Sub Division', 'SubDivision', 'Phân nhóm'])
  val_col = find_col(df_clean, ['Tổng tiền', 'Giá trị sau CK']) or 'Tổng tiền'
  status_col = find_col(df_clean, ['Tình trạng đơn hàng', 'Trạng thái'])

  if sub_div_col:
    df_clean['Mapped_Cat'] = (
        df_clean[sub_div_col].map(sub_map).fillna(df_clean[sub_div_col])
    )
  else:
    df_clean['Mapped_Cat'] = 'Khác'
  df_clean['Mã CH_str'] = df_clean['Mã CH'].astype(str).str.strip()

  df_valid = (
      df_clean[df_clean[status_col] != 'Đã hủy'] if status_col else df_clean
  )
  agg_cat1 = (
      df_valid.groupby(['Mã CH_str', 'Mapped_Cat'])[val_col]
      .sum()
      .reset_index()
  )
  agg_cat1.columns = ['Outlet_key', 'Cat_Key', 'Val1']

  df_closed = (
      df_clean[df_clean[status_col] == 'Đã đóng'] if status_col else df_clean
  )
  agg_cat2 = (
      df_closed.groupby(['Mã CH_str', 'Mapped_Cat'])[val_col]
      .sum()
      .reset_index()
  )
  agg_cat2.columns = ['Outlet_key', 'Cat_Key', 'Val2']

  df_out = df_cat.copy()
  c_code = find_col(df_out, ['Outlet Code', 'Outlet_code', 'Mã CH'])
  c_cat = find_col(df_out, ['Danh sách full cat', 'Category', 'Cat'])
  col_val1 = find_col(
      df_out, ['Doanh số thực đạt của CAT', 'Doanh số thực đạt CAT']
  )
  col_val2 = find_col(
      df_out,
      [
          'Doanh số thực đạt của CAT(Not Cancel/Pending)',
          'Doanh số thực đạt của CAT (Not Cancel/Pending)',
      ],
  )

  if not c_code or not c_cat:
    return df_out
  df_out['_outlet_key'] = df_out[c_code].astype(str).str.strip()
  df_out['_cat_key'] = df_out[c_cat].astype(str).str.strip()

  df_out = df_out.merge(
      agg_cat1,
      left_on=['_outlet_key', '_cat_key'],
      right_on=['Outlet_key', 'Cat_Key'],
      how='left',
  )
  if 'Outlet_key' in df_out.columns:
    df_out = df_out.drop(columns=['Outlet_key', 'Cat_Key'])
  df_out = df_out.merge(
      agg_cat2,
      left_on=['_outlet_key', '_cat_key'],
      right_on=['Outlet_key', 'Cat_Key'],
      how='left',
  )
  if 'Outlet_key' in df_out.columns:
    df_out = df_out.drop(columns=['Outlet_key', 'Cat_Key'])

  if col_val1:
    df_out[col_val1] = df_out['Val1'].fillna(0.0)
  if col_val2:
    df_out[col_val2] = df_out['Val2'].fillna(0.0)

  drop_cols = [
      c
      for c in ['_outlet_key', '_cat_key', 'Val1', 'Val2']
      if c in df_out.columns
  ]
  return df_out.drop(columns=drop_cols)


def process_brand_sales(df_rpt, df_brand):
  if df_brand is None or df_brand.empty or df_rpt is None or df_rpt.empty:
    return df_brand if df_brand is not None else pd.DataFrame()

  # Tìm cột danh sách brand linh hoạt
  c_brand_col = [
      c
      for c in df_brand.columns
      if 'brand' in str(c).lower() and ('danh sách' in str(c).lower() or 'danh sach' in str(c).lower() or 'full' in str(c).lower())
  ]
  if not c_brand_col:
    c_brand_col = [
        c for c in df_brand.columns
        if str(c).strip().lower() in (
            'danh sách full brand', 'danh sach full brand', 'brand', 'nhãn', 'nhãn hàng', 'ten brand'
        )
    ]
  if not c_brand_col:
    # fallback: cột đầu tiên không phải mã/code
    for c in df_brand.columns:
      cl = str(c).lower()
      if 'mã' in cl or 'code' in cl or 'stt' in cl:
        continue
      c_brand_col = [c]
      break
  if not c_brand_col:
    return df_brand
  brand_col_name = c_brand_col[0]
  if brand_col_name not in df_brand.columns:
    return df_brand
  brands_list = df_brand[brand_col_name].dropna().unique().tolist()
  if not brands_list:
    return df_brand

  def match_brand(sku_str):
    if pd.isna(sku_str):
      return 'Khác'
    s = str(sku_str).lower()
    sorted_brands = sorted(brands_list, key=len, reverse=True)
    for b in sorted_brands:
      b_clean = str(b).lower()
      if b_clean in s:
        return b
      if b_clean == 'vinacafe' and (
          'vinacafé' in s
          or 'vinacafe' in s
          or 'phil' in s
          or 'sài gòn' in s
          or 'sai gon' in s
      ):
        return b
      if b_clean == 'wake up 247' and (
          'wake up 247' in s or 'wake-up 247' in s
      ):
        return b
      if b_clean == 'wake up' and ('wake up' in s and '247' not in s):
        return b
      if b_clean == 'heo cao bồi' and ('cao bồi' in s or 'cao boi' in s):
        return b
      if b_clean == 'bupnon tea365' and (
          'búp non' in s or 'tea 365' in s or 'tea365' in s
      ):
        return b
      if b_clean == 'sư tử trắng' and ('sư tử' in s or 'su tu' in s):
        return b
      if b_clean == 'tam thái tử' and ('tam thái tử' in s or 'tam thai tu' in s):
        return b
      if b_clean == 'vivant' and (
          'vivant' in s or 'vĩnh hảo' in s or 'vinh hao' in s
      ):
        return b
      if b_clean == 'compact' and (
          'compact' in s or 'lemona' in s
      ):
        return b
    return 'Khác'

  df_clean = df_rpt.copy()
  sku_col1_list = [c for c in df_clean.columns if 'group std' in str(c).lower()]
  sku_col2_list = [c for c in df_clean.columns if 'tên sản phẩm' in str(c).lower()]
  sku_col1 = sku_col1_list[0] if sku_col1_list else (
      sku_col2_list[0] if sku_col2_list else None
  )
  sku_col2 = sku_col2_list[0] if sku_col2_list else sku_col1
  if sku_col1 is None or sku_col1 not in df_clean.columns:
    return df_brand
  if sku_col2 is None or sku_col2 not in df_clean.columns:
    sku_col2 = sku_col1

  df_clean['Search_Str'] = (
      df_clean[sku_col1].astype(str) + ' ' + df_clean[sku_col2].astype(str)
  )
  val_col_list = [
      c
      for c in df_clean.columns
      if 'tổng tiền' in str(c).lower() or 'giá trị sau ck' in str(c).lower()
      or 'sales after' in str(c).lower() or 'doanh số' in str(c).lower()
  ]
  if not val_col_list:
    return df_brand
  val_col = val_col_list[0]
  status_col = (
      [c for c in df_clean.columns if 'tình trạng đơn hàng' in c.lower()][0]
      if any('tình trạng đơn hàng' in c.lower() for c in df_clean.columns)
      else None
  )

  df_clean['Mapped_Brand'] = df_clean['Search_Str'].apply(match_brand)
  df_clean['Mã CH_str'] = df_clean['Mã CH'].astype(str).str.strip()

  df_valid = (
      df_clean[df_clean[status_col] != 'Đã hủy'] if status_col else df_clean
  )
  agg_b1 = (
      df_valid.groupby(['Mã CH_str', 'Mapped_Brand'])[val_col]
      .sum()
      .reset_index()
  )
  agg_b1.columns = ['Outlet_key', 'Brand_Key', 'Val1']

  df_closed = (
      df_clean[df_clean[status_col] == 'Đã đóng'] if status_col else df_clean
  )
  agg_b2 = (
      df_closed.groupby(['Mã CH_str', 'Mapped_Brand'])[val_col]
      .sum()
      .reset_index()
  )
  agg_b2.columns = ['Outlet_key', 'Brand_Key', 'Val2']

  df_out = df_brand.copy()
  c_code_list = [
      c
      for c in df_out.columns
      if 'outlet code' in str(c).lower()
      or 'mã ch' in str(c).lower()
      or 'ma ch' in str(c).lower()
      or str(c).lower().strip() in ('outlet_code', 'outlet code', 'mã kh', 'ma kh')
  ]
  if not c_code_list:
    return df_brand
  c_code = c_code_list[0]
  c_brand = brand_col_name
  col_val1_list = [
      c
      for c in df_out.columns
      if 'doanh số thực đạt của brand' in str(c).lower() and 'not' not in str(c).lower()
  ]
  col_val2_list = [
      c
      for c in df_out.columns
      if 'doanh số thực đạt của brand' in str(c).lower() and 'not' in str(c).lower()
  ]
  # Fallback tên cột doanh số brand phổ biến
  if not col_val1_list:
    col_val1_list = [
        c for c in df_out.columns
        if 'doanh số' in str(c).lower() and 'brand' in str(c).lower() and 'not' not in str(c).lower()
    ]
  if not col_val2_list:
    col_val2_list = [
        c for c in df_out.columns
        if 'doanh số' in str(c).lower() and 'brand' in str(c).lower() and 'not' in str(c).lower()
    ]
  if not col_val1_list:
    return df_brand
  col_val1 = col_val1_list[0]
  col_val2 = col_val2_list[0] if col_val2_list else col_val1

  df_out['_outlet_key'] = df_out[c_code].astype(str).str.strip()
  df_out['_brand_key'] = df_out[c_brand].astype(str).str.strip()

  df_out = df_out.merge(
      agg_b1,
      left_on=['_outlet_key', '_brand_key'],
      right_on=['Outlet_key', 'Brand_Key'],
      how='left',
  )
  if 'Outlet_key' in df_out.columns:
    df_out = df_out.drop(columns=['Outlet_key', 'Brand_Key'])
  df_out = df_out.merge(
      agg_b2,
      left_on=['_outlet_key', '_brand_key'],
      right_on=['Outlet_key', 'Brand_Key'],
      how='left',
  )
  if 'Outlet_key' in df_out.columns:
    df_out = df_out.drop(columns=['Outlet_key', 'Brand_Key'])

  if col_val1:
    df_out[col_val1] = df_out['Val1'].fillna(0.0)
  if col_val2:
    df_out[col_val2] = df_out['Val2'].fillna(0.0)

  drop_cols = [
      c
      for c in ['_outlet_key', '_brand_key', 'Val1', 'Val2']
      if c in df_out.columns
  ]
  return df_out.drop(columns=drop_cols)



# ====================== MOQ RULES (Công văn T10.2026) ======================
# pattern (regex, lowercase), min_qty, unit: 'le' = Tổng lẻ / SL lẻ, 'chan' = Tổng chẵn / SL Chẵn
MOQ_RULES = [
    # Seasoning
    (r'nước tương.*tam thái tử|nuoc tuong.*tam thai tu', 6, 'le'),
    (r'nước tương.*chinsu|nuoc tuong.*chinsu', 6, 'le'),
    (r'nước mắm nam ngư.*đệ ii.*thùng|nuoc mam nam ngu.*de ii.*thung', 1, 'chan'),
    (r'nước mắm nam ngư.*đệ ii|nuoc mam nam ngu.*de ii', 6, 'le'),
    (r'nước mắm nam ngư.*siêu tiết kiệm can|nuoc mam.*sieu tiet kiem can', 3, 'le'),
    (r'nước mắm nam ngư.*siêu tiết kiệm|nuoc mam.*sieu tiet kiem', 1, 'chan'),
    (r'nước mắm nam ngư.*nhãn vàng|nuoc mam.*nhan vang', 3, 'le'),
    (r'nước mắm nam ngư.*đặc sản|nuoc mam.*dac san', 3, 'le'),
    (r'nước mắm nam ngư.*thủy tinh|nuoc mam.*thuy tinh', 3, 'le'),
    (r'nước mắm nam ngư|nuoc mam nam ngu', 6, 'le'),
    (r'nước mắm chinsu.*cá hồi|nuoc mam chinsu.*ca hoi', 3, 'le'),
    (r'nước mắm chinsu.*biển đông|nuoc mam chinsu.*bien dong', 3, 'le'),
    (r'nước chấm nam ngư|nuoc cham nam ngu', 6, 'le'),
    (r'xốt chinsu|xot chinsu|sốt chinsu', 1, 'le'),
    (r'hạt nêm chinsu', 6, 'le'),
    (r'sa tế chinsu|sa te chinsu', 6, 'le'),
    (r'xốt nhà hàng|xot nha hang', 1, 'le'),
    (r'mayonnaise chinsu|xốt mayonnaise', 6, 'le'),
    (r'muối tôm chinsu|muoi tom chinsu', 3, 'le'),
    (r'xốt muối ớt|xot muoi ot', 6, 'le'),
    (r'kho quẹt nam ngư|kho quet', 4, 'le'),
    (r'dầu hào.*820|dau hao.*820', 4, 'le'),
    (r'dầu hào.*400|dau hao.*400', 6, 'le'),
    (r'dầu hào.*150|dau hao.*150', 6, 'le'),
    (r'dầu hào|dau hao', 6, 'le'),
    (r'tương cà.*250|tuong ca.*250', 8, 'le'),
    (r'tương cà.*500|tuong ca.*500', 6, 'le'),
    (r'tương ớt.*professional|tuong ot.*professional|2\.1kg', 2, 'le'),
    (r'tương ớt.*can|tuong ot.*can', 2, 'le'),
    (r'tương ớt.*1kg|tuong ot.*1kg', 3, 'le'),
    (r'tương ớt.*500|tuong ot.*500', 6, 'le'),
    (r'tương ớt.*250|tuong ot.*250', 8, 'le'),
    (r'tương ớt|tuong ot', 6, 'le'),
    # Home Care
    (r'bột giặt joins.*2\.7|bot giat joins.*2\.7', 2, 'le'),
    (r'bột giặt joins|bot giat joins', 6, 'le'),
    (r'super net.*bột|bot.*super net', 1, 'le'),
    (r'combo.*bột giặt|combo.*bot giat', 2, 'le'),
    (r'bột giặt net|bot giat net', 2, 'le'),
    (r'nước giặt super net|nuoc giat super net', 1, 'le'),
    (r'nước giặt net|nuoc giat net', 2, 'le'),
    (r'nước giặt xả joins|nuoc giat xa joins', 2, 'le'),
    (r'nước lau sàn|nuoc lau san', 2, 'le'),
    (r'combo.*nước rửa chén|combo.*nuoc rua chen', 3, 'le'),
    (r'nước rửa chén net pro|nuoc rua chen net pro', 3, 'le'),
    (r'nước rửa chén.*sạch|nuoc rua chen.*sach', 3, 'le'),
    (r'nước rửa chén net|nuoc rua chen net', 3, 'le'),
    (r'sữa rửa chén homey|sua rua chen homey', 3, 'le'),
    (r'nước rửa chén homey|nuoc rua chen homey', 4, 'le'),
    (r'nước giặt xả homey.*2\.9|homey.*2\.9|homey.*jeju', 2, 'le'),
    (r'nước giặt xả homey|nuoc giat xa homey', 2, 'le'),
    (r'nước giặt xả chanté|nuoc giat xa chante|chanté active|chante active', 2, 'le'),
    (r"sữa tắm la'?petal.*dây|sua tam.*day", 6, 'le'),
    (r"sữa tắm la'?petal|sua tam la.?petal", 2, 'le'),
    # Coffee
    (r'phil 2in1|phil 2 in 1', 4, 'le'),
    (r'vinacafe special 3 in 1.*hộp|vinacafé special.*hộp', 4, 'le'),
    (r'vinacafe special 3 in 1|vinacafé special', 1, 'le'),
    (r'wake up white coffee', 4, 'le'),
    (r'wake up mekong', 4, 'le'),
    (r'vinacafé chất|vinacafe chat', 4, 'le'),
    (r'vinacafé 3in1|vinacafe 3in1|vinacafe 3 in 1', 4, 'le'),
    (r'wake up sài gòn|wake up sai gon', 4, 'le'),
    (r'wake up hương chồn|wake up huong chon', 4, 'le'),
    # Nutrition
    (r"b'?fast canxi|bfast canxi", 4, 'le'),
    (r"sữa b'?fast|sua b.?fast", 24, 'le'),
    (r"ngũ cốc b'?fast|ngu coc b.?fast|b'?fast", 4, 'le'),
    # Processed Meats
    (r'thịt viên|thit vien', 2, 'le'),
    (r'thịt áp chảo|thit ap chao', 2, 'le'),
    (r'snack ponnie', 2, 'le'),
    (r'xúc xích.*19gr|xuc xich.*19', 4, 'le'),
    (r'xúc xích.*70gr|xuc xich.*70', 4, 'le'),
    (r'xúc xích.*bò 35|xuc xich.*bo 35', 4, 'le'),
    (r'xúc xích.*35gr|xuc xich.*35', 4, 'le'),
    (r'cao bồi cuốn|cao boi cuon|cao bồi lắc|cao boi lac', 4, 'le'),
    (r'heo cao bồi xì xèo|heo cao boi', 4, 'le'),
    (r'bin.?bon|bin & bon', 4, 'le'),
    (r'chân gà ponnie|chan ga ponnie', 10, 'le'),
    (r'hotdog ponnie', 1, 'le'),
    # Convenience Foods - thùng
    (r'mì trộn kokomi|mi tron kokomi', 1, 'chan'),
    (r'mì trộn omachi|mi tron omachi', 1, 'chan'),
    (r'sợi tam hoa|soi tam hoa', 1, 'chan'),
    (r'omachi special', 1, 'chan'),
    (r'omachi quán xá|omachi quan xa', 6, 'le'),
    (r'omachi premium', 1, 'chan'),
    (r'mì nấu omachi|mi nau omachi', 1, 'chan'),
    (r'omachi ly lẩu|omachi ly lau', 12, 'le'),
    (r'omachi gói|omachi goi', 1, 'chan'),
    (r'snacking kokomi', 10, 'le'),
    (r'kokomi đại 90 thường ngày|kokomi dai 90.*thịt', 12, 'le'),
    (r'kokomi đại 90|kokomi dai 90', 1, 'chan'),
    (r'kokomi 65', 1, 'chan'),
    (r'kokomi 75', 1, 'chan'),
    (r'komi ly|kokomi ly', 12, 'le'),
    (r'mì trộn komi|mi tron komi', 1, 'chan'),
    (r'phở story|pho story', 1, 'chan'),
    (r'cháo chinsu story|chao chinsu', 15, 'le'),
    (r'bánh phở chinsu|banh pho chinsu', 6, 'le'),
    # Beer
    (r'bia lush|lush', 1, 'chan'),
    (r'white lion', 1, 'chan'),
    (r'red ruby', 1, 'chan'),
    # Refreshment
    (r'faith|chanh muối', 12, 'le'),
    (r'lemona', 12, 'le'),
    (r'vĩnh hảo|vinh hao', 12, 'le'),
    (r'vivant', 12, 'le'),
    (r'wake up 247', 12, 'le'),
    (r'compact', 6, 'le'),
    (r'búp non|bup non|tea\s*365|tea365', 6, 'le'),
]

# Nhóm dual-MOQ (tổng nhóm + từng SKU) — Công văn mục 8.2
DUAL_MOQ_GROUPS = [
    {
        'name': 'omachi_hop_ly',
        'pattern': r'omachi.*(hộp|ly|hộp thịt|ly thịt)',
        'group_min': 12,
        'sku_min': 4,
        'unit': 'le',
    },
    {
        'name': 'omachi_to',
        'pattern': r'omachi.*(tô|to trộn|tô trộn)',
        'group_min': 6,
        'sku_min': 4,
        'unit': 'le',
    },
    {
        'name': 'cao_boi_xot_lac',
        'pattern': r'cao bồi xốt lắc|cao boi xot lac',
        'group_min': 12,
        'sku_min': 3,
        'unit': 'le',
    },
    {
        'name': 'cao_boi',
        'pattern': r'xúc xích cao bồi|xuc xich cao boi|cao bồi(?! xốt)',
        'group_min': 2,
        'sku_min': 1,
        'unit': 'le',
    },
    {
        'name': 'tea365',
        'pattern': r'búp non|bup non|tea\s*365|tea365',
        'group_min': 12,
        'sku_min': 6,
        'unit': 'le',
    },
    {
        'name': 'compact',
        'pattern': r'compact',
        'group_min': 12,
        'sku_min': 6,
        'unit': 'le',
    },
]


def _qty_for_moq(row, unit):
  """Lấy số lượng theo ĐVT MOQ."""
  if unit == 'chan':
    for c in ['Tổng chẵn', 'SL Chẵn', 'SL chẵn']:
      if c in row.index:
        v = pd.to_numeric(row[c], errors='coerce')
        if pd.notna(v):
          return float(v)
  for c in ['Tổng lẻ', 'SL lẻ', 'SL Lẻ']:
    if c in row.index:
      v = pd.to_numeric(row[c], errors='coerce')
      if pd.notna(v):
        return float(v)
  return 0.0


def line_meets_moq(row):
  """True nếu 1 dòng SP trên đơn đạt MOQ riêng (không cộng dồn SP khác)."""
  name = str(row.get('Tên sản phẩm', '') or '').lower()
  if not name or name == 'nan':
    return False
  for pattern, min_qty, unit in MOQ_RULES:
    if re.search(pattern, name, flags=re.IGNORECASE):
      qty = _qty_for_moq(row, unit)
      return qty >= min_qty
  # Không khớp rule nào: coi đạt nếu có số lượng > 0 (SP khác ngoài bảng)
  qty = _qty_for_moq(row, 'le') or _qty_for_moq(row, 'chan')
  return qty > 0


def apply_dual_moq_mask(df_order_lines):
  """Với SP thuộc nhóm dual-MOQ: phải đạt cả MOQ từng SKU và tổng nhóm trên đơn.
  df_order_lines: các dòng cùng 1 đơn hàng.
  Trả về Series bool index = df_order_lines.index (True = line đạt).
  """
  ok = df_order_lines.apply(line_meets_moq, axis=1)
  name = df_order_lines['Tên sản phẩm'].astype(str).str.lower()
  for grp in DUAL_MOQ_GROUPS:
    mask = name.str.contains(grp['pattern'], na=False, regex=True)
    if not mask.any():
      continue
    # sku-level already in line_meets_moq via MOQ_RULES; enforce group total
    unit = grp['unit']
    total = 0.0
    for idx in df_order_lines.index[mask]:
      total += _qty_for_moq(df_order_lines.loc[idx], unit)
    if total < grp['group_min']:
      ok.loc[mask] = False
  return ok


def count_moq_lines_per_order(df_src):
  """Trả DataFrame: Mã NVBH, Mã CH, date, Mã đơn hàng, n_moq_lines."""
  if df_src is None or df_src.empty:
    return pd.DataFrame(
        columns=['Mã NVBH', 'Mã CH', 'date', 'Mã đơn hàng', 'n_moq_lines']
    )
  d = df_src.copy()
  if 'Tên SP lower' not in d.columns:
    d['Tên SP lower'] = d['Tên sản phẩm'].astype(str).str.lower()

  rows = []
  group_cols = ['Mã NVBH', 'Mã CH', 'date', 'Mã đơn hàng']
  for keys, g in d.groupby(group_cols, sort=False):
    ok = apply_dual_moq_mask(g)
    n = int(ok.sum())
    rows.append({
        'Mã NVBH': keys[0],
        'Mã CH': keys[1],
        'date': keys[2],
        'Mã đơn hàng': keys[3],
        'n_moq_lines': n,
    })
  return pd.DataFrame(rows)




def pick_best_pc_per_outlet_day(ok_orders):
  """Max 1 PC/CH/ngày; ưu tiên đơn có số line cao nhất."""
  if ok_orders is None or ok_orders.empty:
    return ok_orders
  df = ok_orders.copy()
  # Chuẩn hóa cột đếm line
  if 'n_moq_lines' not in df.columns:
    # groupby nunique thường để tên cột là tên SKU col
    for c in list(df.columns):
      if c not in ('Mã NVBH', 'Mã CH', 'date', 'Mã đơn hàng'):
        df = df.rename(columns={c: 'n_moq_lines'})
        break
  if 'n_moq_lines' not in df.columns:
    df['n_moq_lines'] = 1
  return (
      df.sort_values('n_moq_lines', ascending=False)
      .drop_duplicates(subset=['Mã NVBH', 'Mã CH', 'date'], keep='first')
  )


def build_report(
    df, report_date, targets, report_type, filter_nv=None, mcp_df=None
):
  title = str(report_type)
  key = str(report_type)
  try:
    _rd0 = report_date if isinstance(report_date, date) else pd.Timestamp(report_date).date()
    _, _, _remain_days, _ = get_timegone_stats(_rd0)
  except Exception:
    _remain_days = 0
  mtd, ngay = pd.Series(dtype=float), pd.Series(dtype=float)
  on_targets = {}
  mcp_off_tgt, mcp_on_tgt = {}, {}
  mtd_off = ngay_off = mtd_on = ngay_on = pd.Series(dtype=float)

  if df is None:
    df = pd.DataFrame()

  if df.empty or 'date' not in df.columns:
    df_mtd = pd.DataFrame()
  else:
    df_mtd = df[
        df['date'] >= date(report_date.year, report_date.month, 1)
    ].copy()
  if nv_selected(filter_nv):
    df_mtd = filter_df_by_nv(df_mtd, 'Tên NVBH', filter_nv)
  if not df_mtd.empty and 'Mã NVBH' in df_mtd.columns:
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())
  else:
    sm_names, all_sms = {}, []
  # Hiển thị đủ NV (kể cả không có đơn → 0)
  sm_names, all_sms = merge_sm_roster(
      sm_names, all_sms, targets=targets, mcp_df=mcp_df
  )
  if nv_selected(filter_nv):
    # giữ filter: chỉ NV được chọn (theo tên hoặc mã)
    vals = filter_nv if isinstance(filter_nv, list) else [filter_nv]
    name_to_code = {v: k for k, v in sm_names.items()}
    keep = set()
    for v in vals:
      v = str(v).strip()
      if v in sm_names:
        keep.add(v)
      elif v in name_to_code:
        keep.add(name_to_code[v])
      else:
        # match by name
        for c, n in sm_names.items():
          if n == v:
            keep.add(c)
    all_sms = [c for c in all_sms if c in keep]

  # ---- Helper: nhận diện ngành hàng ----
  def _is_beer(row_sub, row_name):
    s = f'{row_sub} {row_name}'.lower()
    return any(x in s for x in ['beer', 'bia ', ' bia', 'lush', 'white lion', 'red ruby'])

  def _is_meat(row_sub, row_name):
    s = f'{row_sub} {row_name}'.lower()
    return any(
        x in s
        for x in [
            'processed meats',
            'thịt chế biến',
            'xúc xích',
            'xuc xich',
            'ponnie',
            'cao bồi',
            'cao boi',
            'hotdog',
            'thịt viên',
            'chân gà',
        ]
    )

  def _pc_by_outlet_day(df_src, min_lines=4, exclude_meat_beer=False):
    """Đếm PC: max 1 đơn/ngày/cửa hàng có >= min_lines line (SKU)."""
    if df_src is None or df_src.empty:
      return pd.Series(dtype=int), pd.Series(dtype=int)
    d = df_src.copy()
    if 'Tên SP lower' not in d.columns and 'Tên sản phẩm' in d.columns:
      d['Tên SP lower'] = d['Tên sản phẩm'].astype(str).str.lower()
    if exclude_meat_beer:
      sub = (
          d['Sub Division'].astype(str)
          if 'Sub Division' in d.columns
          else pd.Series('', index=d.index)
      )
      name = (
          d['Tên SP lower']
          if 'Tên SP lower' in d.columns
          else pd.Series('', index=d.index)
      )
      is_ex = sub.str.contains(
          'Beer|Bia|Processed Meats|Thịt chế biến', case=False, na=False
      ) | name.str.contains(
          'beer|bia lush|white lion|red ruby|xúc xích|ponnie|cao bồi|hotdog',
          na=False,
      )
      d = d[~is_ex]
    if d.empty:
      return pd.Series(dtype=int), pd.Series(dtype=int)
    sku_col = 'Mã sản phẩm' if 'Mã sản phẩm' in d.columns else 'Tên sản phẩm'
    lines = d.groupby(['Mã NVBH', 'Mã CH', 'date', 'Mã đơn hàng'])[
        sku_col
    ].nunique()
    ok = lines[lines >= min_lines].reset_index()
    # Đặt tên cột đếm line = n_moq_lines
    count_col = [c for c in ok.columns if c not in ('Mã NVBH', 'Mã CH', 'date', 'Mã đơn hàng')]
    if count_col:
      ok = ok.rename(columns={count_col[0]: 'n_moq_lines'})
    ok_day = pick_best_pc_per_outlet_day(ok)
    mtd_s = ok_day.groupby('Mã NVBH').size()
    ngay_s = ok_day[ok_day['date'] == report_date].groupby('Mã NVBH').size()
    return mtd_s, ngay_s

  def _aso_coverage(df_src, product_pattern, min_qty=1):
    """Số CH có bao phủ SP theo pattern (ASO)."""
    if df_src.empty:
      return pd.Series(dtype=int), pd.Series(dtype=int)
    d = df_src.copy()
    if 'Tên SP lower' not in d.columns:
      parts = []
      for c in ['Tên sản phẩm', 'Group STD', 'Group std', 'STANDARD_SKU_NAME',
                'Tên SP', 'Item name', 'Product name']:
        if c in d.columns:
          parts.append(d[c].astype(str))
      if parts:
        from functools import reduce
        d['Tên SP lower'] = reduce(lambda a, b: a + ' ' + b, parts).str.lower()
      else:
        d['Tên SP lower'] = ''
    mask = d['Tên SP lower'].str.contains(product_pattern, na=False, regex=True)
    d = d[mask]
    if d.empty:
      return pd.Series(dtype=int), pd.Series(dtype=int)
    qty_col = None
    for c in ['Tổng lẻ', 'Số lượng', 'Qty', 'SL']:
      if c in d.columns:
        qty_col = c
        break
    if qty_col:
      d['_qty'] = pd.to_numeric(d[qty_col], errors='coerce').fillna(0)
      ch = d.groupby(['Mã NVBH', 'Mã CH'])['_qty'].sum()
      ch = ch[ch >= min_qty]
    else:
      ch = d.groupby(['Mã NVBH', 'Mã CH']).size()
      ch = ch[ch >= 1]
    ch = ch.reset_index()
    mtd = ch.groupby('Mã NVBH')['Mã CH'].nunique()
    # first buy day for "ngày"
    first = (
        d.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
    )
    first.columns = ['Mã NVBH', 'Mã CH', 'first_date']
    ngay = (
        first[first['first_date'] == report_date]
        .groupby('Mã NVBH')['Mã CH']
        .nunique()
    )
    return mtd, ngay

  def _lppc(df_src, meat_only=False):
    """LPPC = Total line / Tổng PC.
    meat_only=False: trừ Meat & Beer, PC >= 4 line
    meat_only=True: chỉ Processed Meats, PC >= 1 line
    """
    if df_src.empty:
      return pd.Series(dtype=float), pd.Series(dtype=float)
    d = df_src.copy()
    if 'Tên SP lower' not in d.columns:
      d['Tên SP lower'] = d['Tên sản phẩm'].astype(str).str.lower()
    sub = (
        d['Sub Division'].astype(str)
        if 'Sub Division' in d.columns
        else pd.Series('', index=d.index)
    )
    name = d['Tên SP lower']
    is_beer = sub.str.contains('Beer|Bia', case=False, na=False) | name.str.contains(
        'beer|bia lush|white lion|red ruby', na=False
    )
    is_meat = sub.str.contains(
        'Processed Meats|Thịt chế biến', case=False, na=False
    ) | name.str.contains(
        'xúc xích|xuc xich|ponnie|cao bồi|cao boi|hotdog|thịt viên|chân gà',
        na=False,
    )
    if meat_only:
      d = d[is_meat]
      min_lines = 1
    else:
      d = d[~(is_beer | is_meat)]
      min_lines = 4
    if d.empty:
      return pd.Series(dtype=float), pd.Series(dtype=float)
    sku_col = 'Mã sản phẩm' if 'Mã sản phẩm' in d.columns else 'Tên sản phẩm'
    # lines per order
    order_lines = d.groupby(
        ['Mã NVBH', 'Mã CH', 'date', 'Mã đơn hàng']
    )[sku_col].nunique()
    ok_orders = order_lines[order_lines >= min_lines].reset_index()
    ok_orders.columns = list(ok_orders.columns[:-1]) + ['n_lines']
    # max 1 PC / outlet / day
    pc_day = ok_orders.drop_duplicates(subset=['Mã NVBH', 'Mã CH', 'date'])
    # total lines on qualifying PCs only
    pc_keys = pc_day.set_index(
        ['Mã NVBH', 'Mã CH', 'date', 'Mã đơn hàng']
    ).index
    # use first order of the day for line count (the one kept as PC)
    line_on_pc = ok_orders.merge(
        pc_day[['Mã NVBH', 'Mã CH', 'date', 'Mã đơn hàng']],
        on=['Mã NVBH', 'Mã CH', 'date', 'Mã đơn hàng'],
        how='inner',
    )
    total_lines = line_on_pc.groupby('Mã NVBH')['n_lines'].sum()
    total_pc = pc_day.groupby('Mã NVBH').size()
    lppc = (total_lines / total_pc).replace([float('inf')], 0).fillna(0)
    # ngày: LPPC of that day only
    pc_today = pc_day[pc_day['date'] == report_date]
    line_today = line_on_pc[line_on_pc['date'] == report_date]
    if pc_today.empty:
      ngay = pd.Series(dtype=float)
    else:
      tl = line_today.groupby('Mã NVBH')['n_lines'].sum()
      tp = pc_today.groupby('Mã NVBH').size()
      ngay = (tl / tp).replace([float('inf')], 0).fillna(0)
    return lppc, ngay

  on_targets = {}
  mcp_off_tgt, mcp_on_tgt = {}, {}
  mtd_off = ngay_off = mtd_on = ngay_on = pd.Series(dtype=int)
  is_lppc = report_type in ('LPPC', 'LPPC_MEAT')

  if report_type == 'ASO_ALL':
    # OFF & ON - bao phủ CH; tách MCP OFF / MCP ON
    def _aso_by_channel(df_src, report_date):
      if df_src is None or df_src.empty:
        return pd.Series(dtype=int), pd.Series(dtype=int)
      m = df_src.groupby('Mã NVBH')['Mã CH'].nunique()
      first = (
          df_src.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
      )
      first.columns = ['Mã NVBH', 'Mã CH', 'first_date']
      n = (
          first[first['first_date'] == report_date]
          .groupby('Mã NVBH')['Mã CH']
          .nunique()
      )
      return m, n

    off_df = df_mtd[
        df_mtd['L1'].astype(str).str.contains('Off', case=False, na=False)
    ]
    on_df = df_mtd[
        df_mtd['L1'].astype(str).str.contains('On', case=False, na=False)
    ]
    mtd_off, ngay_off = _aso_by_channel(off_df, report_date)
    mtd_on, ngay_on = _aso_by_channel(on_df, report_date)
    # T09: ASO ALL = Kênh OFF only | T10: toàn bộ
    if get_month_cfg().get('aso_all_channel') == 'OFF':
      mtd, ngay = mtd_off.copy(), ngay_off.copy()
    else:
      mtd, ngay = _aso_by_channel(df_mtd, report_date)

    # MCP OFF / ON từ master MCP (số CH theo NV)
    # Chỉ Tiêu MCP = MCP OFF + MCP ON (tổng CH trên MCP)
    mcp_off_tgt, mcp_on_tgt = {}, {}
    if mcp_df is not None and not mcp_df.empty:
      c_code = find_col(mcp_df, ['SM Code', 'Mã NVBH', 'SM code'])
      c_name = find_col(
          mcp_df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên']
      )
      c_l1 = find_col(mcp_df, ['L1', 'Channel'])
      c_ma = find_col(mcp_df, ['Outlet_code', 'Outlet Code', 'Mã CH'])
      if c_l1 and c_ma and (c_code or c_name):
        tmp = mcp_df.copy()
        tmp['_l1'] = tmp[c_l1].astype(str)
        tmp['_ma'] = tmp[c_ma].astype(str).str.strip()
        name_to_code = {v: k for k, v in sm_names.items()}
        # ưu tiên map theo Mã NVBH
        if c_code:
          tmp['_key'] = tmp[c_code].astype(str).str.strip()
        else:
          tmp['_key'] = tmp[c_name].astype(str).str.strip().map(
              lambda x: name_to_code.get(x, x)
          )
        # nếu key là tên thì map sang mã
        def _to_code(k):
          k = str(k).strip()
          if k in sm_names:
            return k
          return name_to_code.get(k, k)

        tmp['_key'] = tmp['_key'].map(_to_code)
        off_m = tmp[tmp['_l1'].str.contains('Off', case=False, na=False)]
        on_m = tmp[tmp['_l1'].str.contains('On', case=False, na=False)]
        mcp_off_tgt = off_m.groupby('_key')['_ma'].nunique().to_dict()
        mcp_on_tgt = on_m.groupby('_key')['_ma'].nunique().to_dict()
        # bổ sung SM có trên MCP nhưng chưa có đơn
        for k in set(list(mcp_off_tgt) + list(mcp_on_tgt)):
          if k not in sm_names:
            # thử lấy tên từ MCP
            if c_name:
              nm = tmp.loc[tmp['_key'] == k, c_name]
              if len(nm):
                sm_names[k] = str(nm.iloc[0]).strip()
            if k not in all_sms:
              all_sms.append(k)
        all_sms = sorted(set(all_sms))

    key, title = 'ASO_ALL', ('ASO_ALL - Kênh OFF' if get_month_cfg().get('aso_all_channel')=='OFF' else 'ASO_ALL - Bao phủ tổng SP Masan (OFF & ON)')

  elif report_type == 'PC_BT':
    # L1 OFF, >=4 line MOQ, max 1 PC/CH/ngày
    # T09 (CV20): trừ Beer | T10: trừ Meat & Beer
    cfg = get_month_cfg()
    off = df_mtd[
        df_mtd['L1'].astype(str).str.contains('Off', case=False, na=False)
    ].copy()
    if 'Tên SP lower' not in off.columns and 'Tên sản phẩm' in off.columns:
      off['Tên SP lower'] = off['Tên sản phẩm'].astype(str).str.lower()
    sub = off['Sub Division'].astype(str) if 'Sub Division' in off.columns else pd.Series('', index=off.index)
    name = off['Tên SP lower'] if 'Tên SP lower' in off.columns else pd.Series('', index=off.index)
    if cfg.get('pc_bt_exclude_meat', True):
      is_ex = sub.str.contains('Beer|Bia|Processed Meats|Thịt chế biến', case=False, na=False) | name.str.contains(
          'beer|bia lush|white lion|red ruby|xúc xích|xuc xich|ponnie|cao bồi|cao boi|hotdog|thịt viên|chân gà', na=False)
    else:
      is_ex = sub.str.contains('Beer|Bia', case=False, na=False) | name.str.contains(
          'beer|bia lush|white lion|red ruby', na=False)
    off = off[~is_ex]
    order_moq = count_moq_lines_per_order(off)
    ok = order_moq[order_moq['n_moq_lines'] >= 1]
    ok_day = pick_best_pc_per_outlet_day(ok)
    mtd = ok_day.groupby('Mã NVBH').size()
    ngay = ok_day[ok_day['date'] == report_date].groupby('Mã NVBH').size()
    key, title = 'PC_BT', 'PC_BT - Đơn hàng ≥1 line MOQ (L1 OFF)'

  elif report_type == 'PC_ON':
    cfg = get_month_cfg()
    if get_month_key() == 'Thang09':
      # T09: ASO Tea Kênh ON — SP Tea/Trà/ô long, MTD >= 12 chai/CH
      on = df_mtd[
          df_mtd['L1'].astype(str).str.contains('On', case=False, na=False)
      ]
      pat = cfg.get('pc_on_pat', r'tea|tr[aà]|ô\s*long|olong')
      min_q = int(cfg.get('pc_on_min_qty', 12) or 12)
      mtd, ngay = _aso_coverage(on if not on.empty else df_mtd, pat, min_qty=min_q)
      key, title = 'PC_ON', cfg.get('pc_on_name', 'ASO_Tea ON')
    else:
      # T10: L1 ON, >=1 line đạt MOQ, max 1 PC/CH/ngày
      on = df_mtd[
          df_mtd['L1'].astype(str).str.contains('On', case=False, na=False)
      ]
      order_moq = count_moq_lines_per_order(on)
      ok = order_moq[order_moq['n_moq_lines'] >= 1]
      ok_day = pick_best_pc_per_outlet_day(ok)
      mtd = ok_day.groupby('Mã NVBH').size()
      ngay = ok_day[ok_day['date'] == report_date].groupby('Mã NVBH').size()
    if mcp_df is not None and not mcp_df.empty:
      c_nv_mcp = find_col(mcp_df, ['SM Code', 'Mã NVBH', 'SM code'])
      c_l1 = find_col(mcp_df, ['L1', 'Channel'])
      c_ma = find_col(mcp_df, ['Outlet_code', 'Outlet Code', 'Mã CH'])
      c_freq = find_col(mcp_df, ['Thứ', 'Frequency', 'Tần suất'])
      if c_nv_mcp and c_l1 and c_ma:
        on_mcp = mcp_df[
            mcp_df[c_l1].astype(str).str.contains('On', case=False, na=False)
        ].copy()
        # PC_ON target = 50% * Số Call; Call ≈ outlets * freq estimate
        # fallback: 50% * số outlet ON
        outlet_cnt = on_mcp.groupby(c_nv_mcp)[c_ma].nunique().to_dict()
        on_targets = {k: int(v * 0.5) for k, v in outlet_cnt.items()}
    key, title = 'PC_ON', 'PC_ON - Đơn hàng ≥1 line MOQ (L1 ON)'

  elif report_type == 'ASO_FOCUS':
    cfg = get_month_cfg()
    key, title = 'ASO_FOCUS', cfg.get('aso_focus_name', 'ASO_Focus')
    if get_month_key() == 'Thang09':
      pat = r'chant[eé]|chante'
    else:
      pat = cfg.get('aso_focus_pat', r'búp non|bup non|tea\s*365|tea365')
    # Tách L1 OFF / ON
    if df_mtd is not None and not df_mtd.empty and 'L1' in df_mtd.columns:
      off_src = df_mtd[df_mtd['L1'].astype(str).str.contains('Off', case=False, na=False)]
      on_src = df_mtd[
          df_mtd['L1'].astype(str).str.contains('On', case=False, na=False)
          & ~df_mtd['L1'].astype(str).str.contains('Off', case=False, na=False)
      ]
    else:
      off_src = pd.DataFrame()
      on_src = pd.DataFrame()
    mtd_off, ngay_off = _aso_coverage(off_src, pat, min_qty=1)
    mtd_on, ngay_on = _aso_coverage(on_src, pat, min_qty=1)
    mtd, ngay = _aso_coverage(
        df_mtd if df_mtd is not None else pd.DataFrame(), pat, min_qty=1
    )

  elif report_type == 'ASO_FOCUS_2':
    cfg = get_month_cfg()
    key, title = 'ASO_FOCUS_2', cfg.get('aso_focus2_name', 'ASO_Focus_2')
    if get_month_key() == 'Thang09':
      # Omachi VÀ Trộn (cùng tên SP)
      d = df_mtd.copy()
      if d.empty:
        mtd, ngay = pd.Series(dtype=int), pd.Series(dtype=int)
      else:
        if 'Tên SP lower' not in d.columns:
          parts = []
          for c in ['Tên sản phẩm', 'Group STD', 'Group std', 'STANDARD_SKU_NAME']:
            if c in d.columns:
              parts.append(d[c].astype(str))
          d['Tên SP lower'] = (' '.join([''] * len(d)) if not parts else None)
          if parts:
            s = parts[0]
            for p in parts[1:]:
              s = s + ' ' + p
            d['Tên SP lower'] = s.str.lower()
          else:
            d['Tên SP lower'] = ''
        mask = (
            d['Tên SP lower'].str.contains(r'omachi', na=False, regex=True)
            & d['Tên SP lower'].str.contains(r'tr[oộ]n|tron', na=False, regex=True)
        )
        d = d[mask]
        if d.empty:
          mtd, ngay = pd.Series(dtype=int), pd.Series(dtype=int)
        else:
          mtd = d.groupby('Mã NVBH')['Mã CH'].nunique()
          first = d.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
          first.columns = ['Mã NVBH', 'Mã CH', 'first_date']
          ngay = first[first['first_date'] == report_date].groupby('Mã NVBH')['Mã CH'].nunique()
    else:
      pat = cfg.get('aso_focus2_pat', r'homey')
      mtd, ngay = _aso_coverage(df_mtd, pat, min_qty=1)

  elif report_type == 'LPPC':
    # Trừ Meat & Beer; line đạt MOQ; PC = đơn ≥1 line MOQ; LPPC = Total line / Tổng PC
    d = df_mtd.copy()
    if 'Tên SP lower' not in d.columns:
      d['Tên SP lower'] = d['Tên sản phẩm'].astype(str).str.lower()
    sub = (
        d['Sub Division'].astype(str)
        if 'Sub Division' in d.columns
        else pd.Series('', index=d.index)
    )
    name = d['Tên SP lower']
    is_ex = sub.str.contains(
        'Beer|Bia|Processed Meats|Thịt chế biến', case=False, na=False
    ) | name.str.contains(
        'beer|bia lush|white lion|red ruby|xúc xích|xuc xich|ponnie|'
        'cao bồi|cao boi|hotdog|thịt viên|chân gà',
        na=False,
    )
    d = d[~is_ex]
    order_moq = count_moq_lines_per_order(d)
    ok = order_moq[order_moq['n_moq_lines'] >= 1]
    ok_day = pick_best_pc_per_outlet_day(ok)
    total_lines = ok_day.groupby('Mã NVBH')['n_moq_lines'].sum()
    total_pc = ok_day.groupby('Mã NVBH').size()
    mtd = (total_lines / total_pc).replace([float('inf')], 0).fillna(0)
    today = ok_day[ok_day['date'] == report_date]
    if today.empty:
      ngay = pd.Series(dtype=float)
    else:
      tl = today.groupby('Mã NVBH')['n_moq_lines'].sum()
      tp = today.groupby('Mã NVBH').size()
      ngay = (tl / tp).replace([float('inf')], 0).fillna(0)
    key, title = 'LPPC', 'LPPC - Bình quân line/PC ≥1 MOQ (trừ Meat & Beer)'

  elif report_type == 'LPPC_MEAT':
    d = df_mtd.copy()
    if 'Tên SP lower' not in d.columns:
      d['Tên SP lower'] = d['Tên sản phẩm'].astype(str).str.lower()
    sub = (
        d['Sub Division'].astype(str)
        if 'Sub Division' in d.columns
        else pd.Series('', index=d.index)
    )
    name = d['Tên SP lower']
    is_meat = sub.str.contains(
        'Processed Meats|Thịt chế biến', case=False, na=False
    ) | name.str.contains(
        'xúc xích|xuc xich|ponnie|cao bồi|cao boi|hotdog|thịt viên|chân gà',
        na=False,
    )
    d = d[is_meat]
    order_moq = count_moq_lines_per_order(d)
    ok = order_moq[order_moq['n_moq_lines'] >= 1]
    ok_day = pick_best_pc_per_outlet_day(ok)
    total_lines = ok_day.groupby('Mã NVBH')['n_moq_lines'].sum()
    total_pc = ok_day.groupby('Mã NVBH').size()
    mtd = (total_lines / total_pc).replace([float('inf')], 0).fillna(0)
    today = ok_day[ok_day['date'] == report_date]
    if today.empty:
      ngay = pd.Series(dtype=float)
    else:
      tl = today.groupby('Mã NVBH')['n_moq_lines'].sum()
      tp = today.groupby('Mã NVBH').size()
      ngay = (tl / tp).replace([float('inf')], 0).fillna(0)
    key, title = 'LPPC_MEAT', 'LPPC_Meat - Bình quân line/PC (Processed Meats)'

  else:
    return pd.DataFrame(), 0, ''

  # Default target theo Công văn nếu không có trong Target_KPI
  DEFAULT_TGT = {
      'ASO_FOCUS': 72,
      'ASO_FOCUS_2': 26,
      'LPPC': 4.7,
      'LPPC_MEAT': 3.8,
  }

  results = []
  for sm in all_sms:
    if report_type == 'PC_ON':
      tgt = targets.get(sm, {}).get('PC_ON', on_targets.get(sm, 0))
    else:
      tgt = targets.get(sm, {}).get(key, DEFAULT_TGT.get(key, 0))
    raw_m = mtd.get(sm, 0)
    raw_n = ngay.get(sm, 0)
    if is_lppc:
      m = round(float(raw_m), 2) if pd.notna(raw_m) else 0
      n = round(float(raw_n), 2) if pd.notna(raw_n) else 0
      tgt_f = float(tgt) if tgt else 0
      pct = round(m / tgt_f * 100, 1) if tgt_f else 0
      ratio = m / tgt_f if tgt_f else 0
    else:
      m = int(raw_m) if pd.notna(raw_m) else 0
      n = int(raw_n) if pd.notna(raw_n) else 0
      tgt = int(tgt) if tgt else 0
      pct = round(m / tgt * 100, 1) if tgt else 0
      ratio = m / tgt if tgt else 0

    if report_type == 'ASO_FOCUS':
      n_off = int(ngay_off.get(sm, 0) or 0)
      m_off = int(mtd_off.get(sm, 0) or 0)
      n_on = int(ngay_on.get(sm, 0) or 0)
      m_on = int(mtd_on.get(sm, 0) or 0)
      pct_off = round(m_off / tgt * 100, 1) if tgt else 0
      pct_on = round(m_on / tgt * 100, 1) if tgt else 0
      _g, _b = _gap_and_bq_day(tgt, m, _remain_days, as_int=True)
      row = {
          'Mã NVBH': sm,
          'Tên NVBH': sm_names.get(sm, ''),
          'Chỉ Tiêu KPI': int(tgt) if not isinstance(tgt, float) else tgt,
          'Thực Hiện Ngày OFF': n_off,
          'MTD OFF': m_off,
          '% MTD OFF': f'{pct_off}%',
          'Thực Hiện Ngày ON': n_on,
          'MTD ON': m_on,
          '% MTD ON': f'{pct_on}%',
          'Thực Hiện Ngày': n,
          'MTD': m,
          '% MTD': f'{pct}%',
          'GAP': _g,
          'Bình quân ngày': _b,
          '_ratio': ratio,
      }
    else:
      row = {
          'Mã NVBH': sm,
          'Tên NVBH': sm_names.get(sm, ''),
          'Chỉ Tiêu KPI': tgt if not is_lppc else float(tgt),
          'Thực Hiện Ngày': n,
          'MTD': m,
          '% MTD': f'{pct}%',
          '_ratio': ratio,
      }
      if report_type not in ('LPPC', 'LPPC_MEAT'):
        _g, _b = _gap_and_bq_day(tgt, m, _remain_days, as_int=True)
        row['GAP'] = _g
        row['Bình quân ngày'] = _b

    if report_type == 'ASO_ALL':
      # Chỉ Tiêu MCP lấy từ Target_KPI (key ASO_ALL)
      nv_name = sm_names.get(sm, '')
      tgt_mcp = int(
          targets.get(sm, {}).get('ASO_ALL', 0) or 0
      )
      t_off = int(mcp_off_tgt.get(sm, 0) or 0)
      t_on = int(mcp_on_tgt.get(sm, 0) or 0)
      m_off = int(mtd_off.get(sm, 0) or 0)
      n_off = int(ngay_off.get(sm, 0) or 0)
      m_on = int(mtd_on.get(sm, 0) or 0)
      n_on = int(ngay_on.get(sm, 0) or 0)
      pct = round(m / tgt_mcp * 100, 1) if tgt_mcp else 0
      ratio = m / tgt_mcp if tgt_mcp else 0
      pct_off = round(m_off / t_off * 100, 1) if t_off else 0
      pct_on = round(m_on / t_on * 100, 1) if t_on else 0
      _gap, _bq = _gap_and_bq_day(tgt_mcp, m, _remain_days, as_int=True)
      row = {
          'Mã NVBH': sm,
          'Tên NVBH': nv_name,
          'Chỉ Tiêu MCP': tgt_mcp,
          'Thực Hiện Ngày': n,
          'MTD': m,
          '% MTD': f'{pct}%',
          'GAP': _gap,
          'Bình quân ngày': _bq,
          'MCP OFF': t_off,
          'Thực hiện ngày OFF': n_off,
          'MTD OFF': m_off,
          '% MTD OFF': f'{pct_off}%',
          'MCP ON': t_on,
          'Thực hiện ngày ON': n_on,
          'MTD ON': m_on,
          '% MTD ON': f'{pct_on}%',
          '_ratio': ratio,
      }
    results.append(row)

  if not results:
    # Không có NV / dữ liệu → trả bảng rỗng an toàn
    empty_cols = (
        [
            'STT', 'Tên NVBH', 'Chỉ Tiêu MCP', 'Thực Hiện Ngày',
            'MTD', '% MTD', 'MCP OFF', 'Thực hiện ngày OFF', 'MTD OFF',
            '% MTD OFF', 'MCP ON', 'Thực hiện ngày ON', 'MTD ON', '% MTD ON',
        ]
        if report_type == 'ASO_ALL'
        else (
            [
                'STT', 'Tên NVBH', 'Chỉ Tiêu KPI',
                'Thực Hiện Ngày OFF', 'MTD OFF', '% MTD OFF',
                'Thực Hiện Ngày ON', 'MTD ON', '% MTD ON',
                'Thực Hiện Ngày', 'MTD', '% MTD',
                'GAP', 'Bình quân ngày',
            ]
            if report_type == 'ASO_FOCUS'
            else (
                [
                    'STT', 'Tên NVBH', 'Chỉ Tiêu KPI',
                    'Thực Hiện Ngày', 'MTD', '% MTD',
                ]
                if report_type in ('LPPC', 'LPPC_MEAT')
                else [
                    'STT', 'Tên NVBH', 'Chỉ Tiêu KPI',
                    'Thực Hiện Ngày', 'MTD', '% MTD',
                    'GAP', 'Bình quân ngày',
                ]
            )
        )
    )
    return pd.DataFrame(columns=empty_cols), 0, title

  df_out = pd.DataFrame(results)
  if '_ratio' in df_out.columns:
    df_out = df_out.sort_values('_ratio', ascending=True).drop(
        columns=['_ratio']
    )
  df_out = df_out.reset_index(drop=True)
  df_out.insert(0, 'STT', range(1, len(df_out) + 1))

  if report_type == 'ASO_ALL':
    total_ngay = int(df_out['Thực Hiện Ngày'].sum()) if not df_out.empty else 0
    total_mtd = int(df_out['MTD'].sum()) if not df_out.empty else 0
    team_tgt = int(df_out['Chỉ Tiêu MCP'].sum()) if not df_out.empty else 0
    total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0
    _show_on = (not df_out.empty) and ('MCP ON' in df_out.columns)
    sum_off = int(df_out['MCP OFF'].sum()) if not df_out.empty and 'MCP OFF' in df_out.columns else 0
    sum_mtd_off = int(df_out['MTD OFF'].sum()) if not df_out.empty and 'MTD OFF' in df_out.columns else 0
    sum_ngay_off = (
        int(df_out['Thực hiện ngày OFF'].sum())
        if not df_out.empty and 'Thực hiện ngày OFF' in df_out.columns else 0
    )
    sum_on = int(df_out['MCP ON'].sum()) if _show_on else 0
    sum_mtd_on = int(df_out['MTD ON'].sum()) if _show_on else 0
    sum_ngay_on = (
        int(df_out['Thực hiện ngày ON'].sum())
        if _show_on and 'Thực hiện ngày ON' in df_out.columns else 0
    )
    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': (
            'SS Trương Thanh Tân Total'
            if not nv_selected(filter_nv)
            else nv_label(filter_nv)
        ),
        'Chỉ Tiêu MCP': team_tgt,
        'Thực Hiện Ngày': total_ngay,
        'MTD': total_mtd,
        '% MTD': f'{total_pct}%',
        'GAP': _gap_and_bq_day(team_tgt, total_mtd, _remain_days, as_int=True)[0],
        'Bình quân ngày': _gap_and_bq_day(team_tgt, total_mtd, _remain_days, as_int=True)[1],
        'MCP OFF': sum_off,
        'Thực hiện ngày OFF': sum_ngay_off,
        'MTD OFF': sum_mtd_off,
        '% MTD OFF': (
            f'{round(sum_mtd_off / sum_off * 100, 1)}%' if sum_off else '0%'
        ),
    }])
    if _show_on:
      total_row.loc[0, 'MCP ON'] = sum_on
      total_row.loc[0, 'Thực hiện ngày ON'] = sum_ngay_on
      total_row.loc[0, 'MTD ON'] = sum_mtd_on
      total_row.loc[0, '% MTD ON'] = (
          f'{round(sum_mtd_on / sum_on * 100, 1)}%' if sum_on else '0%'
      )
    return pd.concat([df_out, total_row], ignore_index=True), team_tgt, title

  if report_type == 'ASO_FOCUS':
    team_tgt = int(df_out['Chỉ Tiêu KPI'].sum()) if not df_out.empty else 0
    total_ngay = int(df_out['Thực Hiện Ngày'].sum()) if not df_out.empty else 0
    total_mtd = int(df_out['MTD'].sum()) if not df_out.empty else 0
    total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0
    sum_ngay_off = int(df_out['Thực Hiện Ngày OFF'].sum()) if 'Thực Hiện Ngày OFF' in df_out.columns else 0
    sum_mtd_off = int(df_out['MTD OFF'].sum()) if 'MTD OFF' in df_out.columns else 0
    sum_ngay_on = int(df_out['Thực Hiện Ngày ON'].sum()) if 'Thực Hiện Ngày ON' in df_out.columns else 0
    sum_mtd_on = int(df_out['MTD ON'].sum()) if 'MTD ON' in df_out.columns else 0
    pct_off = round(sum_mtd_off / team_tgt * 100, 1) if team_tgt else 0
    pct_on = round(sum_mtd_on / team_tgt * 100, 1) if team_tgt else 0
    _g, _b = _gap_and_bq_day(team_tgt, total_mtd, _remain_days, as_int=True)
    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': (
            'SS Trương Thanh Tân Total'
            if not nv_selected(filter_nv)
            else nv_label(filter_nv)
        ),
        'Chỉ Tiêu KPI': team_tgt,
        'Thực Hiện Ngày OFF': sum_ngay_off,
        'MTD OFF': sum_mtd_off,
        '% MTD OFF': f'{pct_off}%',
        'Thực Hiện Ngày ON': sum_ngay_on,
        'MTD ON': sum_mtd_on,
        '% MTD ON': f'{pct_on}%',
        'Thực Hiện Ngày': total_ngay,
        'MTD': total_mtd,
        '% MTD': f'{total_pct}%',
        'GAP': _g,
        'Bình quân ngày': _b,
    }])
    ordered = [
        'STT', 'Tên NVBH', 'Chỉ Tiêu KPI',
        'Thực Hiện Ngày OFF', 'MTD OFF', '% MTD OFF',
        'Thực Hiện Ngày ON', 'MTD ON', '% MTD ON',
        'Thực Hiện Ngày', 'MTD', '% MTD',
        'GAP', 'Bình quân ngày',
    ]
    for c in ordered:
      if c not in df_out.columns:
        df_out[c] = 0 if c not in ('Tên NVBH', 'STT', '% MTD OFF', '% MTD ON', '% MTD') else ''
    df_out = df_out[[c for c in ordered if c in df_out.columns]]
    total_row = total_row[[c for c in ordered if c in total_row.columns]]
    return pd.concat([df_out, total_row], ignore_index=True), team_tgt, title

  if is_lppc:
    total_ngay = (
        round(float(df_out['Thực Hiện Ngày'].mean()), 2)
        if not df_out.empty
        else 0
    )
    total_mtd = (
        round(float(df_out['MTD'].mean()), 2) if not df_out.empty else 0
    )
    team_tgt = (
        round(float(df_out['Chỉ Tiêu KPI'].mean()), 2)
        if not df_out.empty
        else 0
    )
  else:
    total_ngay = int(df_out['Thực Hiện Ngày'].sum()) if not df_out.empty else 0
    total_mtd = int(df_out['MTD'].sum()) if not df_out.empty else 0
    team_tgt = int(df_out['Chỉ Tiêu KPI'].sum()) if not df_out.empty else 0
  total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0
  _tot = {
      'STT': '-',
      'Mã NVBH': 'TỔNG CỘNG',
      'Tên NVBH': (
          'SS Trương Thanh Tân Total'
          if not nv_selected(filter_nv)
          else nv_label(filter_nv)
      ),
      'Chỉ Tiêu KPI': team_tgt,
      'Thực Hiện Ngày': total_ngay,
      'MTD': total_mtd,
      '% MTD': f'{total_pct}%',
  }
  if report_type not in ('LPPC', 'LPPC_MEAT'):
    _g, _b = _gap_and_bq_day(team_tgt, total_mtd, _remain_days, as_int=True)
    _tot['GAP'] = _g
    _tot['Bình quân ngày'] = _b
  total_row = pd.DataFrame([_tot])
  df_out = filter_out_cdgt_smvl(df_out)
  return pd.concat([df_out, total_row], ignore_index=True), team_tgt, title



def _gap_and_bq_day(target, mtd, remain_days, as_int=True):
  """GAP = Chỉ tiêu - MTD; Bình quân ngày = GAP / số ngày bán hàng còn lại.
  remain_days <= 0 → BQ = GAP.
  """
  try:
    gap = float(target or 0) - float(mtd or 0)
  except Exception:
    gap = 0.0
  try:
    rd = int(remain_days or 0)
  except Exception:
    rd = 0
  bq = (gap / rd) if rd > 0 else gap
  if as_int:
    return int(round(gap)), round(bq, 1)
  return gap, round(bq, 1)



@st.cache_data(ttl=600)
def load_weekly_sales():
  """Load file bán hàng lịch sử cho Weekly Preview (data-2 / WeeklyPreview_Sales)."""
  preferred = [
      'data-2-2.xlsx', 'data-2-2.xls',
      'data-2.xlsx', 'data-2.xls',
      'WeeklyPreview_Sales.xlsx', 'WeeklyPreview_Sales.xls',
      'Weekly_Sales.xlsx', 'WEEKLY_SALES.xlsx',
  ]
  path = None
  for name in preferred:
    p = os.path.join(get_data_dir(), name)
    if os.path.isfile(p):
      path = p
      break
  if path is None and os.path.isdir(get_data_dir()):
    try:
      for fn in sorted(os.listdir(get_data_dir())):
        low = fn.lower().replace(' ', '')
        if not low.endswith(('.xlsx', '.xls', '.xlsm')):
          continue
        if 'weekly' in low or 'data-2' in low or low.startswith('data2'):
          path = os.path.join(get_data_dir(), fn)
          break
    except Exception:
      pass
  if not path:
    return pd.DataFrame()
  for hdr in (2, 0, 1, 3):
    try:
      df = pd.read_excel(path, header=hdr)
      cols_up = [str(c).upper().replace(' ', '_') for c in df.columns]
      has_outlet = any('OUTLET' in c and 'CODE' in c for c in cols_up)
      has_sm = any('SM_NAME' in c or c == 'SMNAME' for c in cols_up)
      has_month = any('MONTH' in c for c in cols_up)
      if has_outlet and (has_sm or has_month):
        return df
    except Exception:
      continue
  try:
    return pd.read_excel(path, header=2)
  except Exception:
    return pd.DataFrame()


def build_weekly_preview(mcp_df, sales_hist, df_rpt=None, filter_nv=None, months=None):
  """Weekly Preview: MCP / ASO / %COV theo tháng, map theo Position code.

  Tách 2 bảng: Kênh OFF và Kênh ON.
  MCP (tháng M): số CH MCP có Created_date <= ngày 4 tháng M (theo Position code + L1).
  ASO (tháng M): số CH unique có đơn trong tháng M (POS_CODE + L1), giống ASO ALL.
  %COV = ASO / MCP * 100.
  Hiển thị Tên NVBH lấy từ MCP hiện tại theo Position code.
  """
  if months is None:
    months = [(2026, 6), (2026, 7), (2026, 8), (2026, 9), (2026, 10)]

  def _empty():
    cols = ['STT', 'Tên NVBH', 'Position code']
    for y, m in months:
      lab = f'{m:02d}/{y}'
      cols += [f'MCP|{lab}', f'ASO|{lab}', f'% COV|{lab}']
    return pd.DataFrame(columns=cols)

  def _nma(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  def _is_off(v):
    s = str(v).lower()
    return 'off' in s

  def _is_on(v):
    s = str(v).lower()
    return 'on' in s and 'off' not in s

  # ---- MCP master: Position code → name, L1, created ----
  pos_name = {}  # pos -> current SM name
  pos_list = []
  mcp_rows = []  # list of dicts for aggregation
  if mcp_df is not None and not mcp_df.empty:
    mcp = mcp_df.copy()
    c_nv = find_col(mcp, ['SM name', 'SM Name', 'Tên NVBH', 'Nhân viên BH'])
    c_ma = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH'])
    c_pos = find_col(mcp, ['Position code', 'Position Code', 'POS_CODE', 'Mã vị trí'])
    c_l1 = find_col(mcp, ['L1', 'x_msc_business_type_l1', 'Kênh', 'Channel'])
    c_created = find_col(mcp, ['Created_date', 'Created Date', 'Ngày tạo', 'Create Date'])
    if c_pos and c_ma:
      mcp['_pos'] = mcp[c_pos].astype(str).str.strip()
      mcp['_ma'] = mcp[c_ma].map(_nma)
      mcp['_nv'] = mcp[c_nv].astype(str).str.strip() if c_nv else mcp['_pos']
      mcp['_l1'] = mcp[c_l1].astype(str) if c_l1 else ''
      if c_created:
        mcp['_created'] = pd.to_datetime(mcp[c_created], errors='coerce')
      else:
        mcp['_created'] = pd.NaT
      mcp = mcp[mcp['_pos'].astype(str).str.lower() != 'nan']
      mcp = mcp[~mcp['_nv'].str.contains('vacant', case=False, na=False)]
      # current name per position (mode / last)
      for pos, g in mcp.groupby('_pos', sort=False):
        names = g['_nv'].dropna().astype(str)
        names = names[names.str.lower() != 'nan']
        if len(names):
          pos_name[pos] = names.iloc[-1]
        else:
          pos_name[pos] = pos
      pos_list = sorted(pos_name.keys())
      mcp_rows = mcp

  # filter by NV name → map to position codes
  if nv_selected(filter_nv) and pos_name:
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    pos_list = [p for p in pos_list if pos_name.get(p, '') in vals]

  def _build_channel(channel):
    """channel: 'OFF' or 'ON'"""
    is_ch = _is_off if channel == 'OFF' else _is_on

    # MCP by pos / month
    mcp_by_month = {f'{m:02d}/{y}': {} for y, m in months}
    if isinstance(mcp_rows, pd.DataFrame) and not mcp_rows.empty:
      sub_mcp = mcp_rows[mcp_rows['_l1'].map(is_ch)] if '_l1' in mcp_rows.columns else mcp_rows
      for y, m in months:
        label = f'{m:02d}/{y}'
        cutoff = pd.Timestamp(year=y, month=m, day=4)
        s = sub_mcp[
            sub_mcp['_created'].notna()
            & (sub_mcp['_created'].dt.normalize() <= cutoff)
        ]
        mcp_by_month[label] = s.groupby('_pos')['_ma'].nunique().to_dict()

    # ASO by pos / month from sales hist
    aso_by_month = {f'{m:02d}/{y}': {} for y, m in months}
    if sales_hist is not None and not sales_hist.empty:
      s = sales_hist.copy()
      c_pos = find_col(s, ['POS_CODE', 'Position code', 'Position Code', 'Mã vị trí'])
      c_out = find_col(s, ['OUTLET_CODE', 'Outlet_code', 'Mã CH', 'Mã KH'])
      c_month = find_col(s, ['Month', 'Tháng', 'YearMonth'])
      c_free = find_col(s, ['FREE_ITEM_FLAG', 'Free Item'])
      c_l1 = find_col(s, ['x_msc_business_type_l1', 'L1', 'Kênh', 'Channel'])
      if c_pos and c_out:
        s['_pos'] = s[c_pos].astype(str).str.strip()
        s['_out'] = s[c_out].map(_nma)
        if c_free:
          s = s[s[c_free].astype(str).str.upper().str.strip() != 'Y']
        if c_l1:
          s = s[s[c_l1].map(is_ch)]
        if c_month:
          s['_ym'] = s[c_month].astype(str).str.strip()
          for y, m in months:
            label = f'{m:02d}/{y}'
            ss = s[s['_ym'] == label]
            if not ss.empty:
              aso_by_month[label] = ss.groupby('_pos')['_out'].nunique().to_dict()

    # ASO from RPT for missing months
    if df_rpt is not None and not df_rpt.empty and 'date' in df_rpt.columns:
      for y, m in months:
        label = f'{m:02d}/{y}'
        if aso_by_month.get(label):
          continue
        try:
          start_d = date(y, m, 1)
          end_d = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
          d = df_rpt[(df_rpt['date'] >= start_d) & (df_rpt['date'] < end_d)].copy()
          if d.empty:
            continue
          c_pos = find_col(d, ['Position code', 'POS_CODE', 'Mã vị trí'])
          c_ch = find_col(d, ['Mã CH', 'Mã Cửa hàng', 'Outlet Code'])
          c_l1 = find_col(d, ['L1', 'x_msc_business_type_l1', 'Kênh'])
          if not c_ch:
            continue
          if c_l1:
            d = d[d[c_l1].map(is_ch)]
          if c_pos:
            d['_pos'] = d[c_pos].astype(str).str.strip()
          else:
            # fallback name → try match pos via pos_name reverse
            c_nv = find_col(d, ['Tên NVBH', 'SM Name', 'SM_NAME'])
            if not c_nv:
              continue
            rev = {v: k for k, v in pos_name.items()}
            d['_pos'] = d[c_nv].astype(str).str.strip().map(lambda x: rev.get(x, ''))
            d = d[d['_pos'] != '']
          d['_ch'] = d[c_ch].map(_nma)
          aso_by_month[label] = d.groupby('_pos')['_ch'].nunique().to_dict()
        except Exception:
          pass

    # positions that have any MCP or ASO on this channel
    pos_ch = set(pos_list)
    for lab in mcp_by_month:
      pos_ch |= set(mcp_by_month[lab].keys())
    for lab in aso_by_month:
      pos_ch |= set(aso_by_month[lab].keys())
    # keep only known positions if we have master list
    if pos_list:
      pos_ch = [p for p in sorted(pos_ch) if p in pos_list]
    else:
      pos_ch = sorted(pos_ch)

    rows = []
    for pos in pos_ch:
      nv = pos_name.get(pos, pos)
      if 'vacant' in str(nv).lower():
        continue
      row = {'Tên NVBH': nv, 'Position code': pos}
      for y, m in months:
        label = f'{m:02d}/{y}'
        mcp_v = int(mcp_by_month.get(label, {}).get(pos, 0) or 0)
        aso_v = int(aso_by_month.get(label, {}).get(pos, 0) or 0)
        cov = round(aso_v / mcp_v * 100, 1) if mcp_v else 0.0
        row[f'MCP|{label}'] = mcp_v
        row[f'ASO|{label}'] = aso_v
        row[f'% COV|{label}'] = f'{cov}%'
        row[f'_cov|{label}'] = cov
      rows.append(row)

    if not rows:
      return _empty()

    df_out = pd.DataFrame(rows)
    last_lab = f'{months[-1][1]:02d}/{months[-1][0]}'
    if f'_cov|{last_lab}' in df_out.columns:
      df_out = df_out.sort_values(f'_cov|{last_lab}', ascending=True).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))

    tot = {'STT': '-', 'Tên NVBH': f'SS Trương Thanh Tân Total ({channel})', 'Position code': ''}
    for y, m in months:
      label = f'{m:02d}/{y}'
      mcp_s = int(df_out[f'MCP|{label}'].sum()) if f'MCP|{label}' in df_out.columns else 0
      aso_s = int(df_out[f'ASO|{label}'].sum()) if f'ASO|{label}' in df_out.columns else 0
      cov = round(aso_s / mcp_s * 100, 1) if mcp_s else 0.0
      tot[f'MCP|{label}'] = mcp_s
      tot[f'ASO|{label}'] = aso_s
      tot[f'% COV|{label}'] = f'{cov}%'
    drop_cols = [c for c in df_out.columns if str(c).startswith('_cov|')]
    df_out = df_out.drop(columns=drop_cols, errors='ignore')
    df_out = pd.concat([df_out, pd.DataFrame([tot])], ignore_index=True)
    return df_out

  return _build_channel('OFF'), _build_channel('ON')




def _normalize_weekly_sales_for_lppc(sales_hist):
  """Chuẩn hóa data-2 → schema gần RPT để dùng count_moq_lines_per_order."""
  if sales_hist is None or sales_hist.empty:
    return pd.DataFrame()
  s = sales_hist.copy()
  # Đổi tên cột
  rename = {}
  col_map = [
      (['ITEM_DESC', 'ITEM_DESC_ENGLISH', 'STANDARD_SKU_DESC', 'Tên sản phẩm'], 'Tên sản phẩm'),
      (['OUTLET_CODE', 'Outlet_code', 'Mã CH'], 'Mã CH'),
      (['ORDER_NUM', 'ORDER_NUMBER', 'Mã đơn hàng'], 'Mã đơn hàng'),
      (['POS_CODE', 'Position code'], 'Position code'),
      (['SM_NAME', 'SM Name'], 'Tên NVBH'),
      (['SUB_DIVISION', 'Sub Division'], 'Sub Division'),
      (['ORDER_DT', 'Order Date'], 'ORDER_DT'),
      (['Month'], 'Month'),
      (['FREE_ITEM_FLAG'], 'FREE_ITEM_FLAG'),
      (['x_msc_business_type_l1', 'L1'], 'L1'),
      (['MOQ_FLAG'], 'MOQ_FLAG'),
      (['STANDARD_SKU_CODE', 'ITEM_CODE', 'Mã sản phẩm'], 'Mã sản phẩm'),
  ]
  for cands, dest in col_map:
    src = find_col(s, cands)
    if src and dest not in s.columns:
      if src == dest:
        continue
      rename[src] = dest
  if rename:
    s = s.rename(columns=rename)
  # Đảm bảo có cột Position code
  if 'Position code' not in s.columns:
    src = find_col(s, ['POS_CODE', 'Position Code', 'Position code'])
    if src:
      s['Position code'] = s[src].astype(str).str.strip()

  # Số lượng → Tổng lẻ / Tổng chẵn
  for raw, dest in [
      (['Total Pieces (Sales & Promo) ', 'Total Pieces (Sales & Promo)', 'Total Pieces'], 'Tổng lẻ'),
      (['Total Cases (Sales & Promo) ', 'Total Cases (Sales & Promo)', 'Total Sales Cases'], 'Tổng chẵn'),
  ]:
    src = find_col(s, raw)
    if src and dest not in s.columns:
      s[dest] = pd.to_numeric(s[src], errors='coerce').fillna(0)

  if 'FREE_ITEM_FLAG' in s.columns:
    s = s[s['FREE_ITEM_FLAG'].astype(str).str.upper().str.strip() != 'Y']

  # Chỉ OFF
  if 'L1' in s.columns:
    s = s[s['L1'].astype(str).str.contains('Off', case=False, na=False)]

  # date
  if 'ORDER_DT' in s.columns:
    s['date'] = pd.to_datetime(s['ORDER_DT'], errors='coerce').dt.date
  elif 'Month' in s.columns:
    s['date'] = pd.NaT

  s['Tên SP lower'] = s['Tên sản phẩm'].astype(str).str.lower() if 'Tên sản phẩm' in s.columns else ''
  return s


def _lppc_from_orders(df_lines):
  """LPPC Weekly:

  - Chỉ L1 OFF (caller đã lọc).
  - Trừ Meat & Beer khỏi toàn bộ tính toán.
  - PC = max 1 PC / CH / ngày: chọn 1 đơn có nhiều line nhất.
  - Line trên ĐH PC = số SKU unique **trên đúng đơn đó** (mọi SP non-free, trừ Meat/Beer;
    KHÔNG chỉ lấy MOQ_FLAG=Y — khớp hệ thống Cty hơn).
  - LPPC = Tổng line ÷ Tổng PC.
  - Không lọc ≥4 line.

  Trả về dict: {pos: {'lppc': float, 'pc': int, 'lines': int}}
  """
  if df_lines is None or df_lines.empty:
    return {}
  d = df_lines.copy()

  # Trừ Meat & Beer
  sub = (
      d['Sub Division'].astype(str).str.lower()
      if 'Sub Division' in d.columns
      else pd.Series('', index=d.index)
  )
  is_ex = sub.str.contains('beer|bia|processed meats|thịt chế biến|thit che bien', na=False, regex=True)
  if 'Tên sản phẩm' in d.columns:
    nm = d['Tên sản phẩm'].astype(str).str.lower()
    is_ex = is_ex | nm.str.contains(
        'beer|bia lush|white lion|red ruby|xúc xích|xuc xich|ponnie|cao bồi|cao boi|hotdog|thịt viên|chan ga|chân gà',
        na=False, regex=True,
    )
  d = d.loc[~is_ex]
  if d.empty:
    return {}

  # Free item
  if 'FREE_ITEM_FLAG' in d.columns:
    d = d[d['FREE_ITEM_FLAG'].astype(str).str.upper().str.strip() != 'Y']

  # Key NV
  if 'Mã NVBH' in d.columns:
    d['_nv'] = d['Mã NVBH'].astype(str).str.strip()
  elif 'Position code' in d.columns:
    d['_nv'] = d['Position code'].astype(str).str.strip()
  elif 'POS_CODE' in d.columns:
    d['_nv'] = d['POS_CODE'].astype(str).str.strip()
  else:
    d['_nv'] = d.get('Tên NVBH', pd.Series('', index=d.index)).astype(str).str.strip()

  ch_col = None
  for c in ['Mã CH', 'OUTLET_CODE', 'Outlet_code', 'Mã Cửa hàng']:
    if c in d.columns:
      ch_col = c
      break
  if ch_col is None:
    return {}
  d['_ch'] = d[ch_col].astype(str).str.strip()

  if 'Mã đơn hàng' not in d.columns:
    return {}
  d['_ord'] = d['Mã đơn hàng'].astype(str).str.strip()

  if 'date' in d.columns:
    d['_dt'] = pd.to_datetime(d['date'], errors='coerce').dt.date
  elif 'ORDER_DT' in d.columns:
    d['_dt'] = pd.to_datetime(d['ORDER_DT'], errors='coerce').dt.date
  else:
    d['_dt'] = pd.NaT

  d = d[
      (d['_nv'] != '') & (d['_nv'].str.lower() != 'nan')
      & (d['_ch'] != '') & (d['_ch'].str.lower() != 'nan')
      & (d['_ord'] != '') & (d['_ord'].str.lower() != 'nan')
      & d['_dt'].notna()
  ]
  if d.empty:
    return {}

  sku_col = None
  for c in ['Mã sản phẩm', 'STANDARD_SKU_CODE', 'ITEM_CODE', 'Tên sản phẩm']:
    if c in d.columns:
      sku_col = c
      break
  if sku_col is None:
    return {}

  # Line = mọi SKU unique trên đơn (đã trừ Meat/Beer + free) — không filter MOQ_FLAG
  order_lines = (
      d.groupby(['_nv', '_ch', '_dt', '_ord'], sort=False)[sku_col]
      .nunique()
      .reset_index(name='n_lines')
  )
  if order_lines.empty:
    return {}

  # 1 PC/CH/ngày: chọn đơn nhiều line nhất; line chỉ của đúng đơn đó
  order_lines = order_lines.sort_values('n_lines', ascending=False)
  pc_day = order_lines.drop_duplicates(subset=['_nv', '_ch', '_dt'], keep='first')

  total_lines = pc_day.groupby('_nv')['n_lines'].sum()
  total_pc = pc_day.groupby('_nv').size()
  out = {}
  for nv in total_pc.index:
    pc = int(total_pc.loc[nv])
    lines = int(total_lines.loc[nv]) if nv in total_lines.index else 0
    lppc = round(lines / pc, 2) if pc else 0.0
    out[str(nv)] = {'lppc': lppc, 'pc': pc, 'lines': lines}
  return out



def build_weekly_lppc(mcp_df, sales_hist, df_rpt=None, filter_nv=None, months=None):
  """Bảng LPPC Weekly — chỉ Kênh OFF, logic giống KPI LPPC, map Position code."""
  if months is None:
    months = [(2026, 6), (2026, 7), (2026, 8), (2026, 9), (2026, 10)]

  empty_cols = ['STT', 'Tên NVBH'] + [x for y, m in months for x in (f'PC|{m:02d}/{y}', f'LPPC|{m:02d}/{y}')]
  empty = pd.DataFrame(columns=empty_cols)

  # Position → name từ MCP
  pos_name = {}
  pos_list = []
  if mcp_df is not None and not mcp_df.empty:
    mcp = mcp_df.copy()
    c_nv = find_col(mcp, ['SM name', 'SM Name', 'Tên NVBH'])
    c_pos = find_col(mcp, ['Position code', 'Position Code', 'POS_CODE'])
    if c_pos:
      mcp['_pos'] = mcp[c_pos].astype(str).str.strip()
      mcp['_nv'] = mcp[c_nv].astype(str).str.strip() if c_nv else mcp['_pos']
      mcp = mcp[~mcp['_nv'].str.contains('vacant', case=False, na=False)]
      for pos, g in mcp.groupby('_pos', sort=False):
        names = g['_nv'].dropna()
        names = names[names.str.lower() != 'nan']
        pos_name[pos] = names.iloc[-1] if len(names) else pos
      pos_list = sorted(pos_name.keys())

  if nv_selected(filter_nv) and pos_name:
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    pos_list = [p for p in pos_list if pos_name.get(p, '') in vals]

  s_norm = _normalize_weekly_sales_for_lppc(sales_hist)
  lppc_by_month = {f'{m:02d}/{y}': {} for y, m in months}

  # Tháng 6-9 từ data-2
  if not s_norm.empty and 'Month' in s_norm.columns:
    for y, m in months:
      label = f'{m:02d}/{y}'
      if m == 10 and y == 2026:
        continue  # tháng 10 lấy RPT
      sub = s_norm[s_norm['Month'].astype(str).str.strip() == label].copy()
      if sub.empty:
        continue
      # Gắn Mã NVBH = Position code (ưu tiên) để map tuyến
      pos_col = None
      for c in ['Position code', 'POS_CODE', 'Position Code']:
        if c in sub.columns:
          pos_col = c
          break
      if pos_col is None:
        pos_col = find_col(sub, ['Position code', 'POS_CODE', 'Position Code'])
      if pos_col:
        sub['Mã NVBH'] = sub[pos_col].astype(str).str.strip()
      elif 'Tên NVBH' in sub.columns:
        sub['Mã NVBH'] = sub['Tên NVBH'].astype(str).str.strip()
      lppc_by_month[label] = _lppc_from_orders(sub)

  # Tháng 10 từ RPT (OFF only)
  if df_rpt is not None and not df_rpt.empty:
    for y, m in months:
      label = f'{m:02d}/{y}'
      if lppc_by_month.get(label):
        continue
      try:
        start_d = date(y, m, 1)
        end_d = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
        d = df_rpt[(df_rpt['date'] >= start_d) & (df_rpt['date'] < end_d)].copy()
        if d.empty:
          continue
        if 'L1' in d.columns:
          d = d[d['L1'].astype(str).str.contains('Off', case=False, na=False)]
        c_pos = find_col(d, ['Position code', 'POS_CODE'])
        if c_pos:
          d['Mã NVBH'] = d[c_pos].astype(str).str.strip()
        else:
          c_nv = find_col(d, ['Tên NVBH', 'SM Name'])
          if c_nv and pos_name:
            rev = {v: k for k, v in pos_name.items()}
            d['Mã NVBH'] = d[c_nv].astype(str).str.strip().map(lambda x: rev.get(x, x))
        if 'MOQ_FLAG' not in d.columns:
          d['MOQ_FLAG'] = 'Y'
        lppc_by_month[label] = _lppc_from_orders(d)
      except Exception:
        pass

  if not pos_list:
    keys = set()
    for lab, mp in lppc_by_month.items():
      keys |= set(mp.keys())
    pos_list = sorted(keys)

  rows = []
  for pos in pos_list:
    nv = pos_name.get(pos, pos)
    if 'vacant' in str(nv).lower():
      continue
    row = {'Tên NVBH': nv, 'Position code': pos}
    for y, m in months:
      label = f'{m:02d}/{y}'
      info = lppc_by_month.get(label, {}).get(pos, {})
      if isinstance(info, dict):
        val = float(info.get('lppc', 0) or 0)
        pc = int(info.get('pc', 0) or 0)
        lines = int(info.get('lines', 0) or 0)
      else:
        try:
          val = float(info or 0)
        except Exception:
          val = 0.0
        pc, lines = 0, 0
      row[f'PC|{label}'] = pc
      row[f'LPPC|{label}'] = round(val, 2)
      row[f'_lines|{label}'] = lines
      row[f'_v|{label}'] = val
    rows.append(row)

  if not rows:
    return empty

  df_out = pd.DataFrame(rows)
  last = f'{months[-1][1]:02d}/{months[-1][0]}'
  if f'_v|{last}' in df_out.columns:
    df_out = df_out.sort_values(f'_v|{last}', ascending=True).reset_index(drop=True)
  df_out.insert(0, 'STT', range(1, len(df_out) + 1))

  # Total team: tổng line / tổng PC (đúng LPPC team), kèm tổng PC
  tot = {'STT': '-', 'Tên NVBH': 'SS Trương Thanh Tân Total (LPPC OFF)', 'Position code': ''}
  for y, m in months:
    label = f'{m:02d}/{y}'
    pc_s = int(pd.to_numeric(df_out[f'PC|{label}'], errors='coerce').fillna(0).sum())
    lines_s = int(pd.to_numeric(df_out[f'_lines|{label}'], errors='coerce').fillna(0).sum())
    tot[f'PC|{label}'] = pc_s
    tot[f'LPPC|{label}'] = round(lines_s / pc_s, 2) if pc_s else 0.0
  drop_cols = [c for c in df_out.columns if str(c).startswith('_')]
  df_out = df_out.drop(columns=drop_cols, errors='ignore')
  df_out = pd.concat([df_out, pd.DataFrame([tot])], ignore_index=True)
  return df_out



def _mcp_vip_outlet_map(mcp_df):
  """Map Mã CH → VIP group (VIP3/VIP5/VIPSI), chỉ Kênh OFF."""
  out = {'VIP3': set(), 'VIP5': set(), 'VIPSI': set()}
  if mcp_df is None or mcp_df.empty:
    return out
  mcp = mcp_df.copy()
  c_ma = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH', 'OUTLET_CODE'])
  c_vip = find_col(mcp, [
      'VIP MCH', 'VIP_MCH', 'VIP', 'Nhóm VIP', 'VIP Group', 'Customer Group',
      'VIP Type', 'Loại VIP', 'Group VIP', 'Cust Group', 'Customer_Group',
      'SEGMENT', 'Segment', 'Hạng KH', 'Hang KH',
  ])
  # fallback: cột nào có giá trị chứa VIP3/VIP5/VIPSI
  if not c_vip:
    for c in mcp.columns:
      try:
        sample = mcp[c].astype(str).str.upper().str.replace(' ', '', regex=False)
        if sample.str.contains('VIP3|VIP5|VIPSI', na=False).any():
          c_vip = c
          break
      except Exception:
        pass
  c_l1 = find_col(mcp, ['L1', 'x_msc_business_type_l1', 'Kênh', 'Channel'])
  if not c_ma or not c_vip:
    return out

  def _nma(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  mcp['_ma'] = mcp[c_ma].map(_nma)
  mcp['_vip'] = mcp[c_vip].astype(str).str.strip().str.upper()
  mcp['_vip'] = (
      mcp['_vip']
      .str.replace(' ', '', regex=False)
      .str.replace('_', '', regex=False)
      .str.replace('-', '', regex=False)
  )
  # VIP SI → VIPSI; VIP3/5 variants
  mcp['_vip'] = mcp['_vip'].replace({
      'VIPSI': 'VIPSI', 'VIPSI.': 'VIPSI',
      'VIP3': 'VIP3', 'VIP03': 'VIP3',
      'VIP5': 'VIP5', 'VIP05': 'VIP5',
  })
  if c_l1:
    mcp = mcp[mcp[c_l1].astype(str).str.contains('Off', case=False, na=False)]
  for g in ('VIP3', 'VIP5', 'VIPSI'):
    if g == 'VIPSI':
      mask = mcp['_vip'].str.contains('VIPSI', case=False, na=False)
    else:
      mask = mcp['_vip'] == g
      # fallback contains if exact empty
      if not mask.any():
        mask = mcp['_vip'].str.contains(g, case=False, na=False) & ~mcp['_vip'].str.contains('VIPSI', case=False, na=False)
    out[g] = set(x for x in mcp.loc[mask, '_ma'].tolist() if x)
  return out



def build_weekly_lppc_vip(mcp_df, sales_hist, df_rpt=None, filter_nv=None, months=None):
  """LPPC OFF tách cột VIP3 / VIP5 / VIPSI theo từng tháng.

  Map Mã CH với Data_MCP (VIP MCH) → lọc đơn OFF → LPPC (trừ Meat/Beer).
  """
  if months is None:
    months = [(2026, 6), (2026, 7), (2026, 8), (2026, 9), (2026, 10)]
  vip_groups = ('VIP3', 'VIP5', 'VIPSI')
  empty_cols = ['STT', 'Tên NVBH']
  for y, m in months:
    lab = f'{m:02d}/{y}'
    for g in vip_groups:
      empty_cols += [f'LPPC {g}|{lab}', f'PC {g}|{lab}']
  empty = pd.DataFrame(columns=empty_cols)

  pos_name = {}
  pos_list = []
  if mcp_df is not None and not mcp_df.empty:
    mcp = mcp_df.copy()
    c_nv = find_col(mcp, ['SM name', 'SM Name', 'Tên NVBH'])
    c_pos = find_col(mcp, ['Position code', 'Position Code', 'POS_CODE'])
    if c_pos:
      mcp['_pos'] = mcp[c_pos].astype(str).str.strip()
      mcp['_nv'] = mcp[c_nv].astype(str).str.strip() if c_nv else mcp['_pos']
      mcp = mcp[~mcp['_nv'].str.contains('vacant', case=False, na=False)]
      for pos, g in mcp.groupby('_pos', sort=False):
        names = g['_nv'].dropna()
        names = names[names.str.lower() != 'nan']
        pos_name[pos] = names.iloc[-1] if len(names) else pos
      pos_list = sorted(pos_name.keys())

  if nv_selected(filter_nv) and pos_name:
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    pos_list = [p for p in pos_list if pos_name.get(p, '') in vals]

  vip_map = _mcp_vip_outlet_map(mcp_df)  # already OFF-only

  s_norm = _normalize_weekly_sales_for_lppc(sales_hist)

  def _nma(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  # lppc_by[label][group][pos] = {lppc, pc, lines}
  lppc_by = {
      f'{m:02d}/{y}': {g: {} for g in vip_groups}
      for y, m in months
  }

  def _run_month(sub, label):
    if sub is None or sub.empty or 'Mã CH' not in sub.columns:
      return
    sub = sub.copy()
    # Chỉ kênh OFF
    if 'L1' in sub.columns:
      sub = sub[sub['L1'].astype(str).str.contains('Off', case=False, na=False)]
    # Trừ Meat/Beer
    if 'Tên SP lower' not in sub.columns and 'Tên sản phẩm' in sub.columns:
      sub['Tên SP lower'] = sub['Tên sản phẩm'].astype(str).str.lower()
    if 'Sub Division' in sub.columns or 'Tên SP lower' in sub.columns:
      sub_s = sub['Sub Division'].astype(str) if 'Sub Division' in sub.columns else pd.Series('', index=sub.index)
      name = sub['Tên SP lower'] if 'Tên SP lower' in sub.columns else pd.Series('', index=sub.index)
      is_ex = sub_s.str.contains(
          'Beer|Bia|Processed Meats|Thịt chế biến', case=False, na=False
      ) | name.str.contains(
          'beer|bia lush|white lion|red ruby|xúc xích|xuc xich|ponnie|'
          'cao bồi|cao boi|hotdog|thịt viên|chân gà',
          na=False,
      )
      sub = sub[~is_ex]
    if sub.empty:
      return
    sub['_ma'] = sub['Mã CH'].map(_nma)
    pos_col = find_col(sub, ['Position code', 'POS_CODE', 'Position Code'])
    if pos_col:
      sub['Mã NVBH'] = sub[pos_col].astype(str).str.strip()
    elif 'Tên NVBH' in sub.columns and pos_name:
      rev = {v: k for k, v in pos_name.items()}
      sub['Mã NVBH'] = sub['Tên NVBH'].astype(str).str.strip().map(lambda x: rev.get(x, x))
    if 'Mã NVBH' not in sub.columns:
      return
    for g in vip_groups:
      outlets = set(vip_map.get(g, set()) or set())
      if not outlets:
        continue
      sg = sub[sub['_ma'].isin(outlets)]
      if sg.empty:
        continue
      try:
        order_moq = count_moq_lines_per_order(sg)
        if order_moq is None or order_moq.empty:
          continue
        ok = order_moq[order_moq['n_moq_lines'] >= 1]
        if ok.empty:
          continue
        ok_day = pick_best_pc_per_outlet_day(ok)
        if ok_day.empty:
          continue
        total_lines = ok_day.groupby('Mã NVBH')['n_moq_lines'].sum()
        total_pc = ok_day.groupby('Mã NVBH').size()
        for pos in total_pc.index:
          pc = int(total_pc.get(pos, 0) or 0)
          lines = int(total_lines.get(pos, 0) or 0)
          lppc = round(lines / pc, 2) if pc else 0.0
          lppc_by[label][g][str(pos).strip()] = {
              'lppc': lppc, 'pc': pc, 'lines': lines,
          }
      except Exception:
        pass

  if not s_norm.empty and 'Month' in s_norm.columns:
    # Chuẩn hóa cột Month → MM/YYYY
    def _norm_month(x):
      s = str(x).strip()
      for sep in ('/', '-', '.'):
        if sep in s:
          parts = s.split(sep)
          if len(parts) >= 2:
            try:
              a, b = int(parts[0]), int(parts[1])
              if a > 12:  # YYYY/M
                return f'{b:02d}/{a}'
              return f'{a:02d}/{b}'
            except Exception:
              pass
      return s
    s_norm = s_norm.copy()
    s_norm['_mon'] = s_norm['Month'].map(_norm_month)
    for y, m in months:
      label = f'{m:02d}/{y}'
      if m == 10 and y == 2026:
        continue
      sub = s_norm[s_norm['_mon'] == label].copy()
      if not sub.empty:
        _run_month(sub, label)

  if df_rpt is not None and not df_rpt.empty:
    for y, m in months:
      label = f'{m:02d}/{y}'
      # fill nếu tháng chưa có data (hoặc tháng hiện tại)
      if any(lppc_by[label][g] for g in vip_groups) and not (m == 10 and y == 2026):
        continue
      try:
        start_d = date(y, m, 1)
        end_d = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
        d = df_rpt[(df_rpt['date'] >= start_d) & (df_rpt['date'] < end_d)].copy()
        if d.empty:
          continue
        if 'L1' in d.columns:
          d = d[d['L1'].astype(str).str.contains('Off', case=False, na=False)]
        # trừ meat/beer giống LPPC weekly
        if 'Tên SP lower' not in d.columns and 'Tên sản phẩm' in d.columns:
          d['Tên SP lower'] = d['Tên sản phẩm'].astype(str).str.lower()
        if 'Sub Division' in d.columns or 'Tên SP lower' in d.columns:
          sub_s = d['Sub Division'].astype(str) if 'Sub Division' in d.columns else pd.Series('', index=d.index)
          name = d['Tên SP lower'] if 'Tên SP lower' in d.columns else pd.Series('', index=d.index)
          is_ex = sub_s.str.contains(
              'Beer|Bia|Processed Meats|Thịt chế biến', case=False, na=False
          ) | name.str.contains(
              'beer|bia lush|white lion|red ruby|xúc xích|xuc xich|ponnie|'
              'cao bồi|cao boi|hotdog|thịt viên|chân gà',
              na=False,
          )
          d = d[~is_ex]
        _run_month(d, label)
      except Exception:
        pass

  if not pos_list:
    keys = set()
    for lab in lppc_by:
      for g in vip_groups:
        keys |= set(lppc_by[lab][g].keys())
    pos_list = sorted(keys)

  rows = []
  for pos in pos_list:
    nv = pos_name.get(pos, pos)
    if 'vacant' in str(nv).lower():
      continue
    row = {'Tên NVBH': nv, 'Position code': pos}
    last_val = 0.0
    for y, m in months:
      label = f'{m:02d}/{y}'
      for g in vip_groups:
        info = lppc_by.get(label, {}).get(g, {}).get(str(pos).strip(), {})
        if not isinstance(info, dict):
          info = {}
        val = float(info.get('lppc', 0) or 0)
        pc = int(info.get('pc', 0) or 0)
        lines = int(info.get('lines', 0) or 0)
        row[f'LPPC {g}|{label}'] = round(val, 2)
        row[f'PC {g}|{label}'] = pc
        row[f'_lines {g}|{label}'] = lines
        last_val = val
      row[f'_v|{label}'] = last_val
    rows.append(row)

  if not rows:
    return empty

  df_out = pd.DataFrame(rows)
  last = f'{months[-1][1]:02d}/{months[-1][0]}'
  if f'_v|{last}' in df_out.columns:
    df_out = df_out.sort_values(f'_v|{last}', ascending=True).reset_index(drop=True)
  df_out.insert(0, 'STT', range(1, len(df_out) + 1))

  tot = {'STT': '-', 'Tên NVBH': 'SS Trương Thanh Tân Total (LPPC VIP OFF)'}
  for y, m in months:
    label = f'{m:02d}/{y}'
    for g in vip_groups:
      pc_s = int(pd.to_numeric(df_out.get(f'PC {g}|{label}', 0), errors='coerce').fillna(0).sum())
      lines_s = int(pd.to_numeric(df_out.get(f'_lines {g}|{label}', 0), errors='coerce').fillna(0).sum())
      tot[f'PC {g}|{label}'] = pc_s
      tot[f'LPPC {g}|{label}'] = round(lines_s / pc_s, 2) if pc_s else 0.0
  drop_cols = [c for c in df_out.columns if str(c).startswith('_') or c == 'Position code']
  df_out = df_out.drop(columns=drop_cols, errors='ignore')
  ordered = ['STT', 'Tên NVBH']
  for y, m in months:
    lab = f'{m:02d}/{y}'
    for g in vip_groups:
      ordered += [f'PC {g}|{lab}', f'LPPC {g}|{lab}']
  ordered = [c for c in ordered if c in df_out.columns]
  df_out = df_out[ordered]
  tot_df = pd.DataFrame([{c: tot.get(c, '') for c in ordered}])
  df_out = pd.concat([df_out, tot_df], ignore_index=True)
  return df_out



def render_weekly_lppc_vip_html(df, timegone_pct=None):
  """Bảng LPPC VIP tách VIP3 / VIP5 / VIPSI theo tháng."""
  if df is None or df.empty:
    return '<p>Không có dữ liệu LPPC VIP OFF.</p>'

  months = []
  seen = set()
  for c in df.columns:
    if isinstance(c, str) and c.startswith('LPPC VIP'):
      lab = c.split('|', 1)[1] if '|' in c else ''
      if lab and lab not in seen:
        seen.add(lab)
        months.append(lab)
  # new format: LPPC VIP3|mm/yyyy
  if not months:
    for c in df.columns:
      if isinstance(c, str) and c.startswith('LPPC VIP') and '|' in c:
        lab = c.split('|', 1)[1]
        if lab not in seen:
          seen.add(lab)
          months.append(lab)
  if not months:
    for c in df.columns:
      if isinstance(c, str) and '|' in c and c.split('|', 1)[0].startswith('LPPC'):
        lab = c.split('|', 1)[1]
        if lab not in seen:
          seen.add(lab)
          months.append(lab)

  vip_groups = []
  for c in df.columns:
    if isinstance(c, str) and c.startswith('LPPC VIP') and '|' in c:
      g = c.split('|', 1)[0].replace('LPPC ', '').strip()
      if g and g not in vip_groups:
        vip_groups.append(g)
  if not vip_groups:
    vip_groups = ['VIP3', 'VIP5', 'VIPSI']

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:6px 5px;font-size:11px;white-space:nowrap;'
  )
  th_month = (
      'background-color:#c53030 !important;color:#ffffff !important;'
      'font-weight:900 !important;text-align:center !important;'
      'border:1px solid #9b2c2c !important;padding:8px 5px;font-size:12px;'
  )
  th_sub = (
      'background-color:#2c5282 !important;color:#ffffff !important;'
      'font-weight:700 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:5px 4px;font-size:10px;white-space:nowrap;'
  )
  td = (
      'border:1px solid #bce2f5 !important;padding:5px 6px;'
      'font-size:11px;text-align:center !important;white-space:nowrap;'
  )
  td_tot = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 5px;font-size:11px;'
  )

  def _cls(val):
    try:
      v = float(val)
    except Exception:
      return '', ''
    try:
      moc = float(get_month_cfg().get('lppc_moc', 4.3) or 4.3)
    except Exception:
      moc = 4.3
    if v < moc:
      return ('pct-red', 'background-color:#fed7d7 !important;color:#742a2a !important;font-weight:700 !important;')
    if v >= moc * 1.05:
      return ('pct-purple', 'background-color:#e9d8fd !important;color:#553c9a !important;font-weight:700 !important;')
    return ('pct-green', 'background-color:#c6f6d5 !important;color:#22543d !important;font-weight:700 !important;')

  max_name = 12
  if 'Tên NVBH' in df.columns:
    for n in df['Tên NVBH'].astype(str):
      max_name = max(max_name, len(n))
  name_w = max(140, min(280, max_name * 9 + 24))
  sticky_stt_h = f'{th}position:sticky;left:0;z-index:6;min-width:44px;max-width:44px;'
  sticky_ten_h = f'{th}position:sticky;left:44px;z-index:6;min-width:{name_w}px;'
  sticky_stt_c = f'{td}position:sticky;left:0;z-index:4;min-width:44px;text-align:center;'
  sticky_ten_c = f'{td}position:sticky;left:44px;z-index:4;min-width:{name_w}px;text-align:left;font-weight:600;'
  sticky_stt_t = f'{td_tot}position:sticky;left:0;z-index:5;min-width:44px;text-align:center;'
  sticky_ten_t = f'{td_tot}position:sticky;left:44px;z-index:5;min-width:{name_w}px;text-align:left;'

  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:12px;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;width:max-content;min-width:100%;">',
      '<thead><tr>',
      f'<th rowspan="2" style="{sticky_stt_h}">STT</th>',
      f'<th rowspan="2" style="{sticky_ten_h}">Tên NVBH</th>',
  ]
  for lab in months:
    html.append(f'<th colspan="{len(vip_groups) * 2}" style="{th_month}">{lab}</th>')
  html.append('</tr><tr>')
  for _ in months:
    for g in vip_groups:
      html.append(f'<th style="{th_sub}">PC {g}</th>')
      html.append(f'<th style="{th_sub}">LPPC {g}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = (
        'TOTAL' in str(row.get('Tên NVBH', '')).upper()
        or 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    )
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr' + (' class="row-total"' if is_tot else '') + '>')
    stt = row.get('STT', '')
    ten = row.get('Tên NVBH', '')
    if is_tot:
      html.append(f'<td class="row-total-cell" style="{sticky_stt_t}">{stt}</td>')
      html.append(f'<td class="row-total-cell" style="{sticky_ten_t}">{ten}</td>')
    else:
      html.append(f'<td style="{sticky_stt_c}background-color:{bg} !important;">{stt}</td>')
      html.append(f'<td style="{sticky_ten_c}background-color:{bg} !important;">{ten}</td>')

    for lab in months:
      for g in vip_groups:
        for prefix in (f'PC {g}', f'LPPC {g}'):
          col = f'{prefix}|{lab}'
          val = row.get(col, '')
          if is_tot:
            html.append(f'<td class="row-total-cell" style="{td_tot}">{val}</td>')
          elif prefix.startswith('LPPC'):
            cls, st_c = _cls(val)
            html.append(f'<td data-colored="1" class="{cls}" style="{td}{st_c}">{val}</td>')
          else:
            html.append(f'<td style="{td}background-color:{bg} !important;">{val}</td>')
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def render_weekly_lppc_html(df, timegone_pct=None):
  """Bảng LPPC Weekly — PC + LPPC theo tháng, format KPI."""
  if df is None or df.empty:
    return '<p>Không có dữ liệu LPPC Weekly.</p>'

  months = []
  seen = set()
  for c in df.columns:
    if isinstance(c, str) and c.startswith('LPPC|'):
      lab = c.split('|', 1)[1]
      if lab not in seen:
        seen.add(lab)
        months.append(lab)

  MOC_LPPC = 4.3

  def _pct_style(lppc_val, lab):
    if lppc_val is None:
      return '', ''
    pct = (lppc_val / MOC_LPPC) * 100.0
    moc = 100.0
    if pct < moc:
      return ('pct-red',
              'background-color:#fed7d7 !important;color:#742a2a !important;font-weight:700 !important;')
    if pct < moc + 5:
      return ('pct-green',
              'background-color:#c6f6d5 !important;color:#22543d !important;font-weight:700 !important;')
    return ('pct-purple',
            'background-color:#e9d8fd !important;color:#553c9a !important;font-weight:700 !important;')

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:6px 5px;font-size:11px;white-space:nowrap;'
  )
  th_sticky = th + 'position:sticky;left:0;z-index:3;'
  th_sticky2 = th + 'position:sticky;left:42px;z-index:3;'
  th_mid = (
      'background-color:#2c5282 !important;color:#ffffff !important;'
      'font-weight:700 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:5px;font-size:11px;'
  )
  td = (
      'border:1px solid #bce2f5 !important;padding:5px 6px;'
      'font-size:11px;text-align:center !important;white-space:nowrap;'
  )
  td_tot = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 5px;font-size:11px;'
  )

  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:12px;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;width:max-content;min-width:100%;">',
      '<thead><tr>',
      f'<th rowspan="2" style="{th_sticky}">STT</th>',
      f'<th rowspan="2" style="{th_sticky2}">Tên NVBH</th>',
  ]
  for lab in months:
    html.append(f'<th colspan="2" style="{th}">{lab}</th>')
  html.append('</tr><tr>')
  for lab in months:
    html.append(f'<th style="{th_mid}">PC</th>')
    html.append(f'<th style="{th_mid}">LPPC</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = 'TOTAL' in str(row.get('Tên NVBH', '')).upper() or 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr' + (' class="row-total"' if is_tot else '') + '>')
    stt, ten = row.get('STT', ''), row.get('Tên NVBH', '')
    if is_tot:
      html.append(f'<td class="row-total-cell" style="{td_tot}position:sticky;left:0;">{stt}</td>')
      html.append(f'<td class="row-total-cell" style="{td_tot}position:sticky;left:42px;text-align:left !important;">{ten}</td>')
    else:
      html.append(f'<td style="{td}background-color:{bg} !important;position:sticky;left:0;">{stt}</td>')
      html.append(f'<td style="{td}background-color:{bg} !important;position:sticky;left:42px;text-align:left !important;font-weight:600;">{ten}</td>')
    for lab in months:
      pc_v = row.get(f'PC|{lab}', 0)
      lp_v = row.get(f'LPPC|{lab}', 0)
      try:
        pc_disp = f'{int(float(pc_v)):,}'.replace(',', '.')
      except Exception:
        pc_disp = str(pc_v)
      try:
        fval = float(lp_v)
        lp_disp = f'{fval:.2f}'.replace('.', ',') if False else f'{fval:.1f}'
        # system shows 1 decimal
        lp_disp = f'{fval:.1f}'
      except Exception:
        fval, lp_disp = None, str(lp_v)
      if is_tot:
        html.append(f'<td class="row-total-cell" style="{td_tot}">{pc_disp}</td>')
        cls, st_c = _pct_style(fval, lab)
        if st_c:
          html.append(f'<td data-colored="1" class="{cls}" style="{td}{st_c}">{lp_disp}</td>')
        else:
          html.append(f'<td class="row-total-cell" style="{td_tot}">{lp_disp}</td>')
      else:
        html.append(f'<td style="{td}background-color:{bg} !important;">{pc_disp}</td>')
        cls, st_c = _pct_style(fval, lab)
        if st_c:
          html.append(f'<td data-colored="1" class="{cls}" style="{td}{st_c}">{lp_disp}</td>')
        else:
          html.append(f'<td style="{td}background-color:{bg} !important;">{lp_disp}</td>')
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def _working_days_in_month(year, month, as_of=None):
  """Số ngày làm việc trong tháng (trừ CN + lễ).

  as_of=None → cả tháng (tháng đã kết thúc).
  as_of=date → chỉ đếm đến as_of (tháng đang chạy / MTD).
  """
  first_day = date(year, month, 1)
  if month == 12:
    last_day = date(year + 1, 1, 1) - timedelta(days=1)
  else:
    last_day = date(year, month + 1, 1) - timedelta(days=1)
  holidays_by_month = {
      (2026, 9): {1, 2},
      (2026, 10): set(),
  }
  holiday_days = holidays_by_month.get((year, month), set())
  end = last_day
  if as_of is not None:
    try:
      end = min(last_day, as_of if isinstance(as_of, date) else as_of.date())
    except Exception:
      end = last_day
  total = 0
  curr = first_day
  while curr <= end:
    if curr.weekday() != 6 and curr.day not in holiday_days:
      total += 1
    curr += timedelta(days=1)
  return max(total, 1)


def _pc_count_from_orders(df_lines):
  """Đếm số PC theo NV — max 1 PC / CH / ngày.

  - Không trừ Meat/Beer
  - Không lọc ≥4 line
  - Chỉ tính CH có ≥1 line đạt MOQ trong ngày (MOQ_FLAG=Y)
  - PC = số cặp unique (Mã CH, date) theo từng NV
  """
  if df_lines is None or df_lines.empty:
    return {}
  d = df_lines.copy()

  if 'Mã NVBH' in d.columns:
    d['_nv'] = d['Mã NVBH'].astype(str).str.strip()
  elif 'Position code' in d.columns:
    d['_nv'] = d['Position code'].astype(str).str.strip()
  elif 'POS_CODE' in d.columns:
    d['_nv'] = d['POS_CODE'].astype(str).str.strip()
  else:
    d['_nv'] = d.get('Tên NVBH', pd.Series('', index=d.index)).astype(str).str.strip()

  # Mã CH
  ch_col = None
  for c in ['Mã CH', 'OUTLET_CODE', 'Outlet_code', 'Mã Cửa hàng']:
    if c in d.columns:
      ch_col = c
      break
  if ch_col is None:
    return {}
  d['_ch'] = d[ch_col].astype(str).str.strip()

  # date
  if 'date' in d.columns:
    d['_dt'] = pd.to_datetime(d['date'], errors='coerce').dt.date
  elif 'ORDER_DT' in d.columns:
    d['_dt'] = pd.to_datetime(d['ORDER_DT'], errors='coerce').dt.date
  else:
    d['_dt'] = pd.NaT

  d = d[
      (d['_nv'] != '') & (d['_nv'].str.lower() != 'nan')
      & (d['_ch'] != '') & (d['_ch'].str.lower() != 'nan')
      & d['_dt'].notna()
  ]
  if d.empty:
    return {}

  # Chỉ giữ line đạt MOQ
  if 'MOQ_FLAG' in d.columns:
    d = d[d['MOQ_FLAG'].astype(str).str.upper().str.strip() == 'Y']
  if d.empty:
    return {}

  # Max 1 PC / CH / ngày: đếm unique (CH, date) theo NV
  uniq = d.drop_duplicates(subset=['_nv', '_ch', '_dt'])
  pcs = uniq.groupby('_nv').size()
  return {str(k): int(v) for k, v in pcs.items()}


def _freq_to_weekdays(freq):
  """Map cột Thứ/Frequency MCP → tập weekday (0=Mon … 6=Sun)."""
  s = str(freq).strip().replace(' ', '').upper()
  if not s or s in ('NAN', 'NONE', ''):
    return set()
  mapping = {
      '25': {0, 3}, '36': {1, 4}, '47': {2, 5},
      '2': {0}, '3': {1}, '4': {2}, '5': {3}, '6': {4}, '7': {5},
      'F8': {0, 1, 2, 3},  # ~4 ngày/tuần
      'F4': {0, 3},        # ~2 ngày/tuần
      'F2': {0},           # ~1 ngày/tuần
  }
  if s in mapping:
    return mapping[s]
  # số thuần 1 chữ số
  if s.isdigit() and len(s) == 1:
    d = int(s)
    # 2→Mon … 7→Sat
    if 2 <= d <= 7:
      return {d - 2}
  return set()


def _count_call_days_in_month(freq, year, month, as_of=None):
  """Số ngày trong tháng (đến as_of nếu có) khớp lịch VT của CH."""
  wds = _freq_to_weekdays(freq)
  if not wds:
    return 0
  first = date(year, month, 1)
  if month == 12:
    last = date(year + 1, 1, 1) - timedelta(days=1)
  else:
    last = date(year, month + 1, 1) - timedelta(days=1)
  if as_of is not None:
    try:
      ad = as_of if isinstance(as_of, date) else as_of.date()
      if ad.year == year and ad.month == month:
        last = min(last, ad)
      elif (ad.year, ad.month) < (year, month):
        return 0
    except Exception:
      pass
  holidays_by_month = {
      (2026, 9): {1, 2},
      (2026, 10): set(),
  }
  hol = holidays_by_month.get((year, month), set())
  cnt = 0
  cur = first
  while cur <= last:
    if cur.day not in hol and cur.weekday() in wds:
      cnt += 1
    cur += timedelta(days=1)
  return cnt


def build_weekly_pc_sm_day(mcp_df, sales_hist, df_rpt=None, filter_nv=None, months=None, report_date=None):
  """Bảng PC/SM/Day theo format: mỗi tháng MCP | CALL PLAN BQ | PC/DAY.

  - MCP: số CH MCP OFF (từ COV MCP OFF / build_weekly_preview)
  - CALL PLAN BQ: tổng lượt VT theo lịch MCP trong tháng ÷ số ngày làm việc
  - PC/DAY: tổng PC OFF (MOQ, max 1 PC/CH/ngày) ÷ số ngày làm việc
  """
  if months is None:
    months = [(2026, 6), (2026, 7), (2026, 8), (2026, 9), (2026, 10)]

  empty_cols = ['STT', 'Tên NVBH']
  for y, m in months:
    lab = f'{m:02d}/{y}'
    empty_cols += [f'MCP|{lab}', f'CALL PLAN BQ|{lab}', f'PC/DAY|{lab}']
  empty = pd.DataFrame(columns=empty_cols)

  pos_name = {}
  pos_list = []
  mcp_rows = pd.DataFrame()
  if mcp_df is not None and not mcp_df.empty:
    mcp = mcp_df.copy()
    c_nv = find_col(mcp, ['SM name', 'SM Name', 'Tên NVBH'])
    c_pos = find_col(mcp, ['Position code', 'Position Code', 'POS_CODE'])
    c_thu = find_col(mcp, ['Thứ', 'Frequency', 'Tần suất'])
    c_l1 = find_col(mcp, ['L1', 'Channel', 'Kênh'])
    c_ma = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    if c_pos:
      mcp['_pos'] = mcp[c_pos].astype(str).str.strip()
      mcp['_nv'] = mcp[c_nv].astype(str).str.strip() if c_nv else mcp['_pos']
      mcp = mcp[~mcp['_nv'].str.contains('vacant', case=False, na=False)]
      # CHỈ Kênh OFF cho CALL PLAN BQ + MCP
      if c_l1:
        _l1s = mcp[c_l1].astype(str)
        mcp = mcp[
            _l1s.str.contains('Off', case=False, na=False)
            & ~_l1s.str.contains(r'\bOn\b', case=False, na=False)
        ]
      else:
        # fallback: cột khác nếu có
        for _c in mcp.columns:
          cl = str(_c).lower()
          if 'kênh' in cl or 'channel' in cl or cl == 'l1':
            _l1s = mcp[_c].astype(str)
            mcp = mcp[_l1s.str.contains('Off', case=False, na=False)]
            break
      mcp['_thu'] = mcp[c_thu].astype(str).str.strip() if c_thu else ''
      mcp['_ma'] = mcp[c_ma].astype(str).str.strip() if c_ma else ''
      for pos, g in mcp.groupby('_pos', sort=False):
        names = g['_nv'].dropna()
        names = names[names.str.lower() != 'nan']
        pos_name[pos] = names.iloc[-1] if len(names) else pos
      pos_list = sorted(pos_name.keys())
      mcp_rows = mcp

  if nv_selected(filter_nv) and pos_name:
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    pos_list = [p for p in pos_list if pos_name.get(p, '') in vals]
    if not mcp_rows.empty:
      mcp_rows = mcp_rows[mcp_rows['_pos'].isin(pos_list)]

  s_norm = _normalize_weekly_sales_for_lppc(sales_hist)

  pc_by_month = {f'{m:02d}/{y}': {} for y, m in months}
  as_of_today = report_date if report_date is not None else date.today()
  try:
    if not isinstance(as_of_today, date):
      as_of_today = as_of_today.date()
  except Exception:
    as_of_today = date.today()
  days_by_month = {}
  for y, m in months:
    lab = f'{m:02d}/{y}'
    if (y, m) == (as_of_today.year, as_of_today.month):
      days_by_month[lab] = _working_days_in_month(y, m, as_of=as_of_today)
    else:
      days_by_month[lab] = _working_days_in_month(y, m, as_of=None)

  if not s_norm.empty and 'Month' in s_norm.columns:
    for y, m in months:
      label = f'{m:02d}/{y}'
      if m == 10 and y == 2026:
        continue
      sub = s_norm[s_norm['Month'].astype(str).str.strip() == label].copy()
      if sub.empty:
        continue
      pos_col = None
      for c in ['Position code', 'POS_CODE', 'Position Code']:
        if c in sub.columns:
          pos_col = c
          break
      if pos_col is None:
        pos_col = find_col(sub, ['Position code', 'POS_CODE'])
      if pos_col:
        sub['Mã NVBH'] = sub[pos_col].astype(str).str.strip()
      elif 'Tên NVBH' in sub.columns:
        sub['Mã NVBH'] = sub['Tên NVBH'].astype(str).str.strip()
      pc_by_month[label] = _pc_count_from_orders(sub)

  if df_rpt is not None and not df_rpt.empty:
    for y, m in months:
      label = f'{m:02d}/{y}'
      if pc_by_month.get(label):
        continue
      try:
        start_d = date(y, m, 1)
        end_d = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
        d = df_rpt[(df_rpt['date'] >= start_d) & (df_rpt['date'] < end_d)].copy()
        if d.empty:
          continue
        if 'L1' in d.columns:
          d = d[d['L1'].astype(str).str.contains('Off', case=False, na=False)]
        c_pos = find_col(d, ['Position code', 'POS_CODE'])
        if c_pos:
          d['Mã NVBH'] = d[c_pos].astype(str).str.strip()
        else:
          c_nv = find_col(d, ['Tên NVBH', 'SM Name'])
          if c_nv and pos_name:
            rev = {v: k for k, v in pos_name.items()}
            d['Mã NVBH'] = d[c_nv].astype(str).str.strip().map(lambda x: rev.get(x, x))
        if 'Mã đơn hàng' not in d.columns:
          c_ord = find_col(d, ['Mã đơn hàng', 'ORDER_NUM', 'Số ĐH'])
          if c_ord:
            d['Mã đơn hàng'] = d[c_ord]
        if 'Mã đơn hàng' in d.columns and 'Mã NVBH' in d.columns:
          if 'MOQ_FLAG' not in d.columns:
            d['MOQ_FLAG'] = 'Y'
          pc_by_month[label] = _pc_count_from_orders(d)
      except Exception:
        pass

  if not pos_list:
    keys = set()
    for lab, mp in pc_by_month.items():
      keys |= set(mp.keys())
    pos_list = sorted(keys)

  # MCP OFF từ COV
  mcp_off_by_name = {f'{m:02d}/{y}': {} for y, m in months}
  mcp_off_by_pos = {f'{m:02d}/{y}': {} for y, m in months}
  try:
    df_cov_off, _ = build_weekly_preview(
        mcp_df, sales_hist, df_rpt=None, filter_nv=None, months=months
    )
    if df_cov_off is not None and not df_cov_off.empty:
      body = df_cov_off[~df_cov_off['Tên NVBH'].astype(str).str.upper().str.contains(
          'TOTAL|TỔNG', na=False, regex=True
      )] if 'Tên NVBH' in df_cov_off.columns else df_cov_off
      for y, m in months:
        label = f'{m:02d}/{y}'
        col = f'MCP|{label}'
        if col not in body.columns:
          continue
        for _, r in body.iterrows():
          nm = str(r.get('Tên NVBH', '')).strip()
          pos_c = str(r.get('Position code', '')).strip()
          try:
            v = int(float(r.get(col, 0) or 0))
          except Exception:
            v = 0
          if nm:
            mcp_off_by_name[label][nm] = v
          if pos_c and pos_c.lower() not in ('', 'nan', 'none'):
            mcp_off_by_pos[label][pos_c] = v
  except Exception:
    pass

  # CALL PLAN BQ: tổng lượt VT theo lịch MCP / số ngày làm việc
  call_bq_by_pos = {f'{m:02d}/{y}': {} for y, m in months}
  if not mcp_rows.empty and '_pos' in mcp_rows.columns:
    for y, m in months:
      label = f'{m:02d}/{y}'
      as_of = as_of_today if (y, m) == (as_of_today.year, as_of_today.month) else None
      wd = days_by_month.get(label, 1) or 1
      for pos, g in mcp_rows.groupby('_pos'):
        total_calls = 0
        for _, r in g.iterrows():
          total_calls += _count_call_days_in_month(r.get('_thu', ''), y, m, as_of=as_of)
        call_bq_by_pos[label][str(pos).strip()] = round(total_calls / wd, 2) if wd else 0.0

  rows = []
  for pos in pos_list:
    nv = pos_name.get(pos, pos)
    if 'vacant' in str(nv).lower():
      continue
    row = {'Tên NVBH': nv, 'Position code': pos}
    for y, m in months:
      label = f'{m:02d}/{y}'
      mcp_v = int(
          mcp_off_by_pos.get(label, {}).get(str(pos).strip(), 0)
          or mcp_off_by_name.get(label, {}).get(str(nv).strip(), 0)
          or 0
      )
      # fallback MCP = count outlets on MCP for pos
      if mcp_v == 0 and not mcp_rows.empty:
        try:
          mcp_v = int((mcp_rows['_pos'] == pos).sum())
        except Exception:
          mcp_v = 0
      call_bq = float(call_bq_by_pos.get(label, {}).get(str(pos).strip(), 0) or 0)
      pc = int(pc_by_month.get(label, {}).get(pos, 0) or 0)
      # also try by name key
      if pc == 0:
        pc = int(pc_by_month.get(label, {}).get(str(nv).strip(), 0) or 0)
      wd = days_by_month.get(label, 1) or 1
      pc_day = round(pc / wd, 2) if wd else 0.0
      row[f'MCP|{label}'] = mcp_v
      row[f'CALL PLAN BQ|{label}'] = call_bq
      row[f'PC/DAY|{label}'] = pc_day
      row[f'_v|{label}'] = pc_day
    rows.append(row)

  if not rows:
    return empty

  df_out = pd.DataFrame(rows)
  last = f'{months[-1][1]:02d}/{months[-1][0]}'
  if f'_v|{last}' in df_out.columns:
    df_out = df_out.sort_values(f'_v|{last}', ascending=True).reset_index(drop=True)
  df_out.insert(0, 'STT', range(1, len(df_out) + 1))

  ordered = ['STT', 'Tên NVBH']
  tot = {'STT': '-', 'Tên NVBH': 'SS Trương Thanh Tân Total'}
  for y, m in months:
    lab = f'{m:02d}/{y}'
    for prefix in ('MCP', 'CALL PLAN BQ', 'PC/DAY'):
      col = f'{prefix}|{lab}'
      ordered.append(col)
      if col in df_out.columns:
        vals = pd.to_numeric(df_out[col], errors='coerce').fillna(0)
        if prefix == 'MCP':
          tot[col] = int(vals.sum())
        else:
          tot[col] = round(float(vals.mean()), 2) if len(vals) else 0.0
  drop_cols = [c for c in df_out.columns if str(c).startswith('_') or c == 'Position code']
  df_out = df_out.drop(columns=drop_cols, errors='ignore')
  ordered = [c for c in ordered if c in df_out.columns]
  df_out = df_out[ordered]
  tot_df = pd.DataFrame([{c: tot.get(c, '') for c in ordered}])
  df_out = pd.concat([df_out, tot_df], ignore_index=True)
  return df_out



def build_weekly_trai_tuyen_mtd(df_rpt, df_visit, mcp_df, report_date, filter_nv=None):
  """Tổng hợp ĐH Trái Tuyến từ đầu tháng → ngày BC theo từng NV.

  % ĐH Trái Tuyến = Số ĐH Trái Tuyến / Tổng PC (MOQ) * 100.
  Check Danh Sách bổ sung = số ĐH có tick / tổng ĐH trái tuyến.
  LPPC BQ Nhóm Bổ Sung = bình quân LPPC các ĐH trái tuyến CÓ trong DS bổ sung.
  LPPC BQ Nhóm Ngoài DS = bình quân LPPC các ĐH trái tuyến KHÔNG trong DS bổ sung.
  """
  empty = pd.DataFrame(columns=[
      'STT', 'Tên NVBH', 'Số ĐH Trái Tuyến', 'Tổng PC',
      '% ĐH Trái Tuyến', 'Check Danh Sách bổ sung',
      'LPPC BQ Nhóm Bổ Sung', 'LPPC BQ Nhóm Ngoài DS',
  ])
  if report_date is None:
    return empty
  rd = report_date.date() if hasattr(report_date, 'date') else report_date
  start = date(rd.year, rd.month, 1)

  parts = []
  cur = start
  while cur <= rd:
    try:
      det = build_trai_tuyen_orders(df_rpt, df_visit, mcp_df, cur, filter_nv=filter_nv)
      if det is not None and not det.empty:
        if 'Tên NVBH' in det.columns:
          det = det[~det['Tên NVBH'].astype(str).str.upper().str.contains('TOTAL|TỔNG', na=False, regex=True)]
        if not det.empty:
          parts.append(det)
    except Exception:
      pass
    cur = cur + timedelta(days=1)

  detail = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()

  pc_by_nv = {}
  if df_rpt is not None and not df_rpt.empty:
    try:
      d = df_rpt.copy()
      if 'date' in d.columns:
        d = d[(d['date'] >= start) & (d['date'] <= rd)]
      if not d.empty:
        if 'L1' in d.columns:
          d = d[d['L1'].astype(str).str.contains('Off', case=False, na=False)]
        order_moq = count_moq_lines_per_order(d)
        ok = order_moq[order_moq['n_moq_lines'] >= 1] if not order_moq.empty else order_moq
        if not ok.empty:
          ok_day = pick_best_pc_per_outlet_day(ok)
          name_map = {}
          if 'Tên NVBH' in d.columns and 'Mã NVBH' in d.columns:
            name_map = d.groupby('Mã NVBH')['Tên NVBH'].first().astype(str).str.strip().to_dict()
          for ma, g in ok_day.groupby('Mã NVBH'):
            nm = name_map.get(ma, str(ma))
            pc_by_nv[nm] = pc_by_nv.get(nm, 0) + int(len(g))
    except Exception:
      pass

  def _is_check(v):
    s = str(v).strip()
    return s in ('✓', '✔', 'Y', 'YES', '1', 'TRUE', 'true') or '✓' in s

  def _to_float(v):
    try:
      s = str(v).replace('%', '').replace(',', '.').strip()
      if not s or s.lower() in ('nan', 'none', ''):
        return None
      return float(s)
    except Exception:
      return None

  trai_cnt = {}
  check_cnt = {}
  lppc_bo_sung = {}  # list of lppc values
  lppc_ngoai = {}

  if detail is not None and not detail.empty and 'Tên NVBH' in detail.columns:
    c_chk = None
    for c in detail.columns:
      cl = str(c).lower()
      if 'bổ sung' in cl or 'bo sung' in cl or 'danh sách' in cl:
        c_chk = c
        break
    c_lppc = None
    for c in detail.columns:
      if str(c).strip().upper() == 'LPPC' or 'lppc' in str(c).lower():
        c_lppc = c
        break

    for nv, g in detail.groupby(detail['Tên NVBH'].astype(str).str.strip()):
      if not nv or nv.lower() in ('nan', 'none'):
        continue
      trai_cnt[nv] = len(g)
      if c_chk:
        mask_chk = g[c_chk].map(_is_check)
        check_cnt[nv] = int(mask_chk.sum())
      else:
        mask_chk = pd.Series(False, index=g.index)
        check_cnt[nv] = 0

      if c_lppc:
        vals_bs = [_to_float(v) for v in g.loc[mask_chk, c_lppc].tolist()]
        vals_out = [_to_float(v) for v in g.loc[~mask_chk, c_lppc].tolist()]
        vals_bs = [v for v in vals_bs if v is not None]
        vals_out = [v for v in vals_out if v is not None]
        lppc_bo_sung[nv] = vals_bs
        lppc_ngoai[nv] = vals_out
      else:
        lppc_bo_sung[nv] = []
        lppc_ngoai[nv] = []

  all_nv = sorted(set(list(trai_cnt.keys()) + list(pc_by_nv.keys())))
  if nv_selected(filter_nv):
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    all_nv = [n for n in all_nv if n in vals]

  rows = []
  for nv in all_nv:
    n_trai = int(trai_cnt.get(nv, 0))
    n_pc = int(pc_by_nv.get(nv, 0))
    pct = round(n_trai / n_pc * 100, 1) if n_pc else 0.0
    n_chk = int(check_cnt.get(nv, 0))
    bs = lppc_bo_sung.get(nv, [])
    out = lppc_ngoai.get(nv, [])
    lppc_bs = round(sum(bs) / len(bs), 2) if bs else 0.0
    lppc_out = round(sum(out) / len(out), 2) if out else 0.0
    rows.append({
        'Tên NVBH': nv,
        'Số ĐH Trái Tuyến': n_trai,
        'Tổng PC': n_pc,
        '% ĐH Trái Tuyến': f'{pct}%',
        'Check Danh Sách bổ sung': f'{n_chk}/{n_trai}' if n_trai else '0/0',
        'LPPC BQ Nhóm Bổ Sung': lppc_bs,
        'LPPC BQ Nhóm Ngoài DS': lppc_out,
        '_pct': pct,
        '_trai': n_trai,
        '_bs_vals': bs,
        '_out_vals': out,
    })

  if not rows:
    return empty

  df_out = pd.DataFrame(rows)
  df_out = df_out.sort_values('_trai', ascending=False).reset_index(drop=True)
  df_out.insert(0, 'STT', range(1, len(df_out) + 1))

  tot_trai = int(df_out['Số ĐH Trái Tuyến'].sum())
  tot_pc = int(df_out['Tổng PC'].sum())
  tot_pct = round(tot_trai / tot_pc * 100, 1) if tot_pc else 0.0
  tot_chk = 0
  for v in df_out['Check Danh Sách bổ sung']:
    try:
      tot_chk += int(str(v).split('/')[0])
    except Exception:
      pass
  all_bs = []
  all_out = []
  for v in df_out.get('_bs_vals', []):
    if isinstance(v, list):
      all_bs.extend(v)
  for v in df_out.get('_out_vals', []):
    if isinstance(v, list):
      all_out.extend(v)
  tot_lppc_bs = round(sum(all_bs) / len(all_bs), 2) if all_bs else 0.0
  tot_lppc_out = round(sum(all_out) / len(all_out), 2) if all_out else 0.0

  tot = {
      'STT': '-',
      'Tên NVBH': 'SS Trương Thanh Tân Total',
      'Số ĐH Trái Tuyến': tot_trai,
      'Tổng PC': tot_pc,
      '% ĐH Trái Tuyến': f'{tot_pct}%',
      'Check Danh Sách bổ sung': f'{tot_chk}/{tot_trai}' if tot_trai else '0/0',
      'LPPC BQ Nhóm Bổ Sung': tot_lppc_bs,
      'LPPC BQ Nhóm Ngoài DS': tot_lppc_out,
  }
  df_out = df_out.drop(columns=[c for c in df_out.columns if str(c).startswith('_')], errors='ignore')
  df_out = pd.concat([df_out, pd.DataFrame([tot])], ignore_index=True)
  return df_out



def render_weekly_trai_tuyen_html(df):
  """Bảng ĐH Trái Tuyến MTD — format sticky giống Trưng Bày."""
  if df is None or df.empty:
    return '<p>Không có dữ liệu ĐH Trái Tuyến MTD.</p>'

  max_name = 12
  if 'Tên NVBH' in df.columns:
    for n in df['Tên NVBH'].astype(str):
      max_name = max(max_name, len(n))
  name_w = max(140, min(280, max_name * 9 + 24))

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 5px;font-size:11px;white-space:nowrap;'
  )
  td = 'border:1px solid #bce2f5 !important;padding:5px 6px;font-size:11px;white-space:nowrap;'
  td_tot = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;border:1px solid #2b6cb0 !important;'
      'padding:6px 5px;font-size:11px;'
  )
  sticky_stt_h = f'{th}position:sticky;left:0;z-index:6;min-width:44px;max-width:44px;'
  sticky_ten_h = f'{th}position:sticky;left:44px;z-index:6;min-width:{name_w}px;'
  sticky_stt_c = f'{td}position:sticky;left:0;z-index:4;min-width:44px;text-align:center;'
  sticky_ten_c = f'{td}position:sticky;left:44px;z-index:4;min-width:{name_w}px;text-align:left;font-weight:600;'
  sticky_stt_t = f'{td_tot}position:sticky;left:0;z-index:5;min-width:44px;text-align:center;'
  sticky_ten_t = f'{td_tot}position:sticky;left:44px;z-index:5;min-width:{name_w}px;text-align:left;'

  def _pct_style(val):
    try:
      v = float(str(val).replace('%', ''))
    except Exception:
      return '', ''
    if v >= 10:
      return ('pct-red', 'background-color:#fc8181 !important;color:#742a2a !important;font-weight:800 !important;')
    if v >= 5:
      return ('pct-red', 'background-color:#fed7d7 !important;color:#742a2a !important;font-weight:700 !important;')
    return ('pct-green', 'background-color:#c6f6d5 !important;color:#22543d !important;font-weight:700 !important;')

  cols = [c for c in df.columns if not str(c).startswith('_')]
  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:12px;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;width:max-content;min-width:100%;">',
      '<thead><tr>',
  ]
  for c in cols:
    if c == 'STT':
      html.append(f'<th style="{sticky_stt_h}">STT</th>')
    elif c == 'Tên NVBH':
      html.append(f'<th style="{sticky_ten_h}">Tên NVBH</th>')
    else:
      html.append(f'<th style="{th}">{c}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = (
        'TOTAL' in str(row.get('Tên NVBH', '')).upper()
        or 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    )
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr' + (' class="row-total"' if is_tot else '') + '>')
    for c in cols:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      if is_tot:
        if c == 'STT':
          html.append(f'<td class="row-total-cell" style="{sticky_stt_t}">{val}</td>')
        elif c == 'Tên NVBH':
          html.append(f'<td class="row-total-cell" style="{sticky_ten_t}">{val}</td>')
        elif c == '% ĐH Trái Tuyến':
          cls, st_c = _pct_style(val)
          html.append(f'<td data-colored="1" class="{cls} row-total-cell" style="{st_c}font-weight:900 !important;text-align:center !important;">{val}</td>')
        else:
          html.append(f'<td class="row-total-cell" style="{td_tot}text-align:center !important;">{val}</td>')
      else:
        if c == 'STT':
          html.append(f'<td style="{sticky_stt_c}background-color:{bg} !important;">{val}</td>')
        elif c == 'Tên NVBH':
          html.append(f'<td style="{sticky_ten_c}background-color:{bg} !important;">{val}</td>')
        elif c == '% ĐH Trái Tuyến':
          cls, st_c = _pct_style(val)
          html.append(f'<td data-colored="1" class="{cls}" style="{td}{st_c}text-align:center !important;">{val}</td>')
        else:
          html.append(f'<td style="{td}background-color:{bg} !important;text-align:center;">{val}</td>')
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def render_weekly_pc_day_html(df):
  """Bảng PC/SM/Day format: mỗi tháng MCP | CALL PLAN BQ | PC/DAY."""
  if df is None or df.empty:
    return '<p>Không có dữ liệu PC/SM/Day.</p>'

  months = []
  seen = set()
  for c in df.columns:
    if isinstance(c, str) and '|' in c:
      lab = c.split('|', 1)[1]
      if lab not in seen:
        seen.add(lab)
        months.append(lab)

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:6px 5px;font-size:11px;white-space:nowrap;'
  )
  th_month = (
      'background-color:#c53030 !important;color:#ffffff !important;'
      'font-weight:900 !important;text-align:center !important;'
      'border:1px solid #9b2c2c !important;padding:8px 5px;font-size:12px;'
  )
  th_sub = (
      'background-color:#2c5282 !important;color:#ffffff !important;'
      'font-weight:700 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:5px 4px;font-size:10px;white-space:nowrap;'
  )
  td = (
      'border:1px solid #bce2f5 !important;padding:5px 6px;'
      'font-size:11px;text-align:center !important;white-space:nowrap;'
  )
  td_tot = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 5px;font-size:11px;'
  )

  # median PC/DAY for color
  body = df.iloc[:-1] if len(df) > 1 else df
  meds = {}
  for lab in months:
    col = f'PC/DAY|{lab}'
    if col not in body.columns:
      col = f'PC/Day|{lab}'
    if col in body.columns:
      vals = pd.to_numeric(body[col], errors='coerce').dropna()
      meds[lab] = float(vals.median()) if len(vals) else 0.0

  def _style_pcday(val, med):
    try:
      v = float(val)
    except Exception:
      return '', ''
    if med is None or med <= 0:
      return '', ''
    ratio = v / med * 100.0
    if ratio < 90:
      return ('pct-red', 'background-color:#fed7d7 !important;color:#742a2a !important;font-weight:700 !important;')
    if ratio < 110:
      return ('pct-green', 'background-color:#c6f6d5 !important;color:#22543d !important;font-weight:700 !important;')
    return ('pct-purple', 'background-color:#e9d8fd !important;color:#553c9a !important;font-weight:700 !important;')

  max_name = 12
  if 'Tên NVBH' in df.columns:
    for n in df['Tên NVBH'].astype(str):
      max_name = max(max_name, len(n))
  name_w = max(140, min(280, max_name * 9 + 24))
  sticky_stt_h = f'{th}position:sticky;left:0;z-index:6;min-width:44px;max-width:44px;'
  sticky_ten_h = f'{th}position:sticky;left:44px;z-index:6;min-width:{name_w}px;'
  sticky_stt_c = f'{td}position:sticky;left:0;z-index:4;min-width:44px;text-align:center;'
  sticky_ten_c = f'{td}position:sticky;left:44px;z-index:4;min-width:{name_w}px;text-align:left;font-weight:600;'
  sticky_stt_t = f'{td_tot}position:sticky;left:0;z-index:5;min-width:44px;text-align:center;'
  sticky_ten_t = f'{td_tot}position:sticky;left:44px;z-index:5;min-width:{name_w}px;text-align:left;'

  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:12px;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;width:max-content;min-width:100%;">',
      '<thead>',
      '<tr>',
      f'<th rowspan="2" style="{sticky_stt_h}">STT</th>',
      f'<th rowspan="2" style="{sticky_ten_h}">Tên NVBH</th>',
  ]
  for lab in months:
    html.append(f'<th colspan="3" style="{th_month}">{lab}</th>')
  html.append('</tr><tr>')
  for _ in months:
    for sub in ('MCP', 'CALL PLAN BQ', 'PC/DAY'):
      html.append(f'<th style="{th_sub}">{sub}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = (
        'TOTAL' in str(row.get('Tên NVBH', '')).upper()
        or 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    )
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr' + (' class="row-total"' if is_tot else '') + '>')
    stt = row.get('STT', '')
    ten = row.get('Tên NVBH', '')
    if is_tot:
      html.append(f'<td class="row-total-cell" style="{sticky_stt_t}">{stt}</td>')
      html.append(f'<td class="row-total-cell" style="{sticky_ten_t}">{ten}</td>')
    else:
      html.append(f'<td style="{sticky_stt_c}background-color:{bg} !important;">{stt}</td>')
      html.append(f'<td style="{sticky_ten_c}background-color:{bg} !important;">{ten}</td>')

    for lab in months:
      for prefix in ('MCP', 'CALL PLAN BQ', 'PC/DAY', 'PC/Day'):
        col = f'{prefix}|{lab}'
        if col not in df.columns:
          continue
        if prefix == 'PC/Day' and f'PC/DAY|{lab}' in df.columns:
          continue
        val = row.get(col, '')
        if is_tot:
          html.append(f'<td class="row-total-cell" style="{td_tot}">{val}</td>')
        elif prefix in ('PC/DAY', 'PC/Day'):
          cls, st_c = _style_pcday(val, meds.get(lab))
          html.append(f'<td data-colored="1" class="{cls}" style="{td}{st_c}">{val}</td>')
        else:
          html.append(f'<td style="{td}background-color:{bg} !important;">{val}</td>')
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def render_weekly_preview_html(df, timegone_pct=None):
  """Bảng Weekly Preview — header 2 tầng, sticky STT/Tên, % format giống Tab KPI."""
  if df is None or df.empty:
    return '<p>Không có dữ liệu Weekly Preview.</p>'

  months = []
  seen = set()
  for c in df.columns:
    if isinstance(c, str) and c.startswith('MCP|'):
      lab = c.split('|', 1)[1]
      if lab not in seen:
        seen.add(lab)
        months.append(lab)

  # Tháng hiện tại (cuối cùng trong list) dùng Timegone; tháng cũ mốc 100%
  cur_lab = months[-1] if months else ''
  try:
    tg = float(timegone_pct) if timegone_pct is not None else float(_CURRENT_TIMEGONE or 100)
  except Exception:
    tg = 100.0

  def _pct_style(pct, lab):
    """Trả (class, style) theo rule KPI: đỏ / xanh / tím."""
    moc = tg if lab == cur_lab else 100.0
    if pct is None:
      return '', ''
    # Đỏ: dưới mốc; Xanh: đạt mốc đến +5; Tím: vượt >5% so với mốc
    if pct < moc:
      return (
          'pct-red',
          'background-color:#fed7d7 !important;color:#742a2a !important;font-weight:700 !important;',
      )
    if pct < moc + 5:
      return (
          'pct-green',
          'background-color:#c6f6d5 !important;color:#22543d !important;font-weight:700 !important;',
      )
    return (
        'pct-purple',
        'background-color:#e9d8fd !important;color:#553c9a !important;font-weight:700 !important;',
    )

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:6px 5px;font-size:11px;'
      'white-space:nowrap;'
  )
  th_sticky = th + 'position:sticky;left:0;z-index:3;'
  th_sticky2 = th + 'position:sticky;left:42px;z-index:3;'
  th_mid = (
      'background-color:#2c5282 !important;color:#ffffff !important;'
      'font-weight:700 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:5px;font-size:11px;'
  )
  td = (
      'border:1px solid #bce2f5 !important;padding:5px 6px;'
      'font-size:11px;text-align:center !important;white-space:nowrap;'
  )
  td_tot = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 5px;font-size:11px;'
  )

  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:12px;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;'
      'width:max-content;min-width:100%;">',
      '<thead>',
      '<tr>',
      f'<th rowspan="2" style="{th_sticky}">STT</th>',
      f'<th rowspan="2" style="{th_sticky2}">Tên NVBH</th>',
  ]
  for lab in months:
    html.append(f'<th colspan="3" style="{th}">{lab}</th>')
  html.append('</tr><tr>')
  for lab in months:
    for sub in ('MCP', 'ASO', '% COV'):
      html.append(f'<th style="{th_mid}">{sub}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = (
        'TOTAL' in str(row.get('Tên NVBH', '')).upper()
        or 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    )
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr' + (' class="row-total"' if is_tot else '') + '>')
    stt = row.get('STT', '')
    ten = row.get('Tên NVBH', '')

    if is_tot:
      html.append(f'<td class="row-total-cell" style="{td_tot}position:sticky;left:0;z-index:1;">{stt}</td>')
      html.append(
          f'<td class="row-total-cell" style="{td_tot}position:sticky;left:42px;z-index:1;'
          f'text-align:left !important;">{ten}</td>'
      )
    else:
      html.append(
          f'<td style="{td}background-color:{bg} !important;position:sticky;left:0;z-index:1;">{stt}</td>'
      )
      html.append(
          f'<td style="{td}background-color:{bg} !important;position:sticky;left:42px;z-index:1;'
          f'text-align:left !important;font-weight:600;">{ten}</td>'
      )

    for lab in months:
      for sub in ('MCP', 'ASO', '% COV'):
        key = f'{sub}|{lab}'
        val = row.get(key, '')
        if pd.isna(val):
          val = ''
        if sub == '% COV':
          try:
            pct = float(str(val).replace('%', '').replace(',', '.').strip())
          except Exception:
            pct = None
          cls, st_c = _pct_style(pct, lab)
          if is_tot:
            # total: giữ nền xanh đậm chữ trắng, nhưng % vẫn tô màu rule
            if st_c:
              html.append(
                  f'<td data-colored="1" class="{cls}" style="{td}{st_c}">{val}</td>'
              )
            else:
              html.append(f'<td class="row-total-cell" style="{td_tot}">{val}</td>')
          else:
            if st_c:
              html.append(
                  f'<td data-colored="1" class="{cls}" style="{td}{st_c}">{val}</td>'
              )
            else:
              html.append(
                  f'<td style="{td}background-color:{bg} !important;">{val}</td>'
              )
        else:
          if is_tot:
            html.append(f'<td class="row-total-cell" style="{td_tot}">{val}</td>')
          else:
            html.append(
                f'<td style="{td}background-color:{bg} !important;">{val}</td>'
            )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def build_turnover_report(df, report_date, turnover_targets, filter_nv=None):
  title = 'TURNOVER - Tổng doanh số bán ra'
  if df is None or df.empty:
    return pd.DataFrame(columns=[
        'STT', 'Tên NVBH', 'Chỉ Tiêu Doanh Số',
        'Thực Hiện Ngày', 'Doanh Số MTD', '% MTD',
        'GAP', 'Bình quân ngày',
    ]), 0.0, title

  try:
    _rd0 = report_date if isinstance(report_date, date) else pd.Timestamp(report_date).date()
    _, _, _remain_days, _ = get_timegone_stats(_rd0)
  except Exception:
    _remain_days = 0
  df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
  df_today = df[df['date'] == report_date].copy()

  if nv_selected(filter_nv):
    df_mtd = filter_df_by_nv(df_mtd, 'Tên NVBH', filter_nv)
    df_today = filter_df_by_nv(df_today, 'Tên NVBH', filter_nv)

  if not df_mtd.empty and 'Mã NVBH' in df_mtd.columns:
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())
  else:
    sm_names, all_sms = {}, []
  sm_names, all_sms = merge_sm_roster(
      sm_names, all_sms, turnover_targets=turnover_targets
  )
  if nv_selected(filter_nv):
    vals = filter_nv if isinstance(filter_nv, list) else [filter_nv]
    name_to_code = {v: k for k, v in sm_names.items()}
    keep = set()
    for v in vals:
      v = str(v).strip()
      if v in sm_names:
        keep.add(v)
      elif v in name_to_code:
        keep.add(name_to_code[v])
      else:
        for c, n in sm_names.items():
          if n == v:
            keep.add(c)
    all_sms = [c for c in all_sms if c in keep]

  val_col = (
      find_col(
          df_mtd, ['Thành tiền trước CK', 'Thành tiền trước chiết khấu']
      )
      or 'Thành tiền trước CK'
  )

  mtd_sales = df_mtd.groupby('Mã NVBH')[val_col].sum().to_dict()
  today_sales = df_today.groupby('Mã NVBH')[val_col].sum().to_dict()

  results = []
  for sm in all_sms:
    tgt = turnover_targets.get(sm, 0.0)
    m = float(mtd_sales.get(sm, 0.0))
    t_val = float(today_sales.get(sm, 0.0))
    pct = round(m / tgt * 100, 1) if tgt else 0.0
    _gap, _bq = _gap_and_bq_day(tgt, m, _remain_days, as_int=False)
    results.append({
        'Mã NVBH': sm,
        'Tên NVBH': sm_names.get(sm, ''),
        'Chỉ Tiêu Doanh Số': tgt,
        'Thực Hiện Ngày': t_val,
        'Doanh Số MTD': m,
        '% MTD': f'{pct}%',
        'GAP': _gap,
        'Bình quân ngày': _bq,
        '_ratio': (m / tgt if tgt else 0),
    })

  df_out = (
      pd.DataFrame(results)
      .sort_values('_ratio', ascending=True)
      .drop(columns=['_ratio'])
      .reset_index(drop=True)
  )
  df_out.insert(0, 'STT', range(1, len(df_out) + 1))

  total_mtd = float(df_out['Doanh Số MTD'].sum()) if not df_out.empty else 0.0
  total_today = (
      float(df_out['Thực Hiện Ngày'].sum()) if not df_out.empty else 0.0
  )
  team_tgt = (
      float(df_out['Chỉ Tiêu Doanh Số'].sum()) if not df_out.empty else 0.0
  )
  total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0.0

  total_row = pd.DataFrame([{
      'STT': '-',
      'Mã NVBH': 'TỔNG CỘNG',
      'Tên NVBH': (
          'SS Trương Thanh Tân Total'
          if not nv_selected(filter_nv)
          else nv_label(filter_nv)
      ),
      'Chỉ Tiêu Doanh Số': team_tgt,
      'Thực Hiện Ngày': total_today,
      'Doanh Số MTD': total_mtd,
      '% MTD': f'{total_pct}%',
      'GAP': _gap_and_bq_day(team_tgt, total_mtd, _remain_days, as_int=False)[0],
      'Bình quân ngày': _gap_and_bq_day(team_tgt, total_mtd, _remain_days, as_int=False)[1],
  }])
  df_out = filter_out_cdgt_smvl(df_out)
  return (
      pd.concat([df_out, total_row], ignore_index=True),
      team_tgt,
      'BÁO CÁO DOANH SỐ TURNOVER',
  )


# ====================== HÀM BÁO CÁO LỊCH VIẾNG THĂM (MỚI) ======================
def build_visit_report(
    df_mcp, df_rpt, report_date, filter_nv=None, f_thu_list=None
):
  if df_mcp.empty:
    return (
        pd.DataFrame(),
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        'BÁO CÁO LỊCH VIẾNG THĂM',
    )

  mcp_f = df_mcp.copy()
  if nv_selected(filter_nv):
    c_nv = find_col(mcp_f, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    if c_nv:
      mcp_f = filter_df_by_nv(mcp_f, c_nv, filter_nv)

  if f_thu_list:
    c_thu = find_col(mcp_f, ['Thứ', 'Frequency', 'Tần suất'])
    mcp_f = filter_by_thu_multi(mcp_f, c_thu, f_thu_list)

  # Lọc theo tuần chẵn/lẻ ISO (cột ODD_WEEK)
  mcp_f = filter_by_odd_week(mcp_f, report_date)

  c_nv_name = (
      find_col(mcp_f, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
      or 'SM name'
  )
  c_nv_code = find_col(mcp_f, ['SM Code', 'Mã NVBH', 'SM code']) or 'SM code'
  c_ma_col = (
      find_col(mcp_f, ['Outlet_code', 'Outlet Code', 'Mã CH']) or 'Outlet_code'
  )
  c_vip = find_col(mcp_f, ['VIP MCH', 'VIP_MCH'])
  c_l1 = find_col(mcp_f, ['L1', 'Channel'])

  df_mtd = (
      df_rpt[df_rpt['date'] >= date(report_date.year, report_date.month, 1)]
      .copy()
      if df_rpt is not None and not df_rpt.empty
      else pd.DataFrame()
  )
  active_ma_set = (
      set(df_mtd['Mã CH'].astype(str).str.strip().unique())
      if not df_mtd.empty
      else set()
  )

  nv_list = (
      sorted(mcp_f[c_nv_name].dropna().astype(str).unique().tolist())
      if c_nv_name in mcp_f.columns
      else []
  )

  rows = []
  for nv in nv_list:
    sub = mcp_f[mcp_f[c_nv_name].astype(str).str.strip() == nv]
    sm_code = (
        sub[c_nv_code].iloc[0]
        if c_nv_code in sub.columns and not sub[c_nv_code].empty
        else ''
    )

    sub_v3 = (
        sub[sub[c_vip].astype(str).str.strip() == 'VIP3'] if c_vip else pd.DataFrame()
    )
    sub_v5 = (
        sub[sub[c_vip].astype(str).str.strip() == 'VIP5'] if c_vip else pd.DataFrame()
    )
    sub_vsi = (
        sub[sub[c_vip].astype(str).str.strip() == 'VIPSI']
        if c_vip
        else pd.DataFrame()
    )
    sub_on = (
        sub[sub[c_l1].astype(str).str.contains('On', case=False, na=False)]
        if c_l1
        else pd.DataFrame()
    )

    off_sub = (
        sub[~sub[c_l1].astype(str).str.contains('On', case=False, na=False)]
        if c_l1
        else sub
    )
    if c_vip:
      sub_le = off_sub[
          ~off_sub[c_vip].astype(str).str.strip().isin(['VIP3', 'VIP5', 'VIPSI'])
      ]
    else:
      sub_le = off_sub

    def get_metrics(sub_subset):
      if sub_subset.empty:
        return 0, 0, '0.0%'
      total_kh = sub_subset[c_ma_col].nunique()
      ma_set = set(sub_subset[c_ma_col].astype(str).str.strip().unique())
      da_mua = len(ma_set.intersection(active_ma_set))
      pct = round(da_mua / total_kh * 100, 1) if total_kh else 0.0
      return total_kh, da_mua, f'{pct}%'

    v3_t, v3_m, v3_p = get_metrics(sub_v3)
    v5_t, v5_m, v5_p = get_metrics(sub_v5)
    vsi_t, vsi_m, vsi_p = get_metrics(sub_vsi)
    le_t, le_m, le_p = get_metrics(sub_le)
    on_t, on_m, on_p = get_metrics(sub_on)

    total_vt = sub[c_ma_col].nunique()
    total_mua = len(
        set(sub[c_ma_col].astype(str).str.strip().unique()).intersection(
            active_ma_set
        )
    )
    total_pct = round(total_mua / total_vt * 100, 1) if total_vt else 0.0

    rows.append({
        'Mã NVBH': sm_code,
        'Tên NVBH': nv,
        'Tổng KH': total_vt,
        'Đã Mua': total_mua,
        '% Active': f'{total_pct}%',
        'VIP3_Tổng': v3_t,
        'VIP3_Mua': v3_m,
        'VIP3_Pct': v3_p,
        'VIP5_Tổng': v5_t,
        'VIP5_Mua': v5_m,
        'VIP5_Pct': v5_p,
        'VIPSI_Tổng': vsi_t,
        'VIPSI_Mua': vsi_m,
        'VIPSI_Pct': vsi_p,
        'Lẻ_Tổng': le_t,
        'Lẻ_Mua': le_m,
        'Lẻ_Pct': le_p,
        'ON_Tổng': on_t,
        'ON_Mua': on_m,
        'ON_Pct': on_p,
        '_sort': total_vt,
    })

  df_out = pd.DataFrame(rows)
  if not df_out.empty:
    df_out = (
        df_out.sort_values('_sort', ascending=False)
        .drop(columns=['_sort'])
        .reset_index(drop=True)
    )
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))

  num_nv = len(df_out)
  tot_vt = int(df_out['Tổng KH'].sum()) if not df_out.empty else 0
  tot_mua = int(df_out['Đã Mua'].sum()) if not df_out.empty else 0
  tot_p = round(tot_mua / tot_vt * 100, 1) if tot_vt else 0.0

  tot_v3_t = int(df_out['VIP3_Tổng'].sum()) if not df_out.empty else 0
  tot_v3_m = int(df_out['VIP3_Mua'].sum()) if not df_out.empty else 0
  tot_v3_p = round(tot_v3_m / tot_v3_t * 100, 1) if tot_v3_t else 0.0

  tot_v5_t = int(df_out['VIP5_Tổng'].sum()) if not df_out.empty else 0
  tot_v5_m = int(df_out['VIP5_Mua'].sum()) if not df_out.empty else 0
  tot_v5_p = round(tot_v5_m / tot_v5_t * 100, 1) if tot_v5_t else 0.0

  tot_vsi_t = int(df_out['VIPSI_Tổng'].sum()) if not df_out.empty else 0
  tot_vsi_m = int(df_out['VIPSI_Mua'].sum()) if not df_out.empty else 0
  tot_vsi_p = round(tot_vsi_m / tot_vsi_t * 100, 1) if tot_vsi_t else 0.0

  tot_le_t = int(df_out['Lẻ_Tổng'].sum()) if not df_out.empty else 0
  tot_le_m = int(df_out['Lẻ_Mua'].sum()) if not df_out.empty else 0
  tot_le_p = round(tot_le_m / tot_le_t * 100, 1) if tot_le_t else 0.0

  tot_on_t = int(df_out['ON_Tổng'].sum()) if not df_out.empty else 0
  tot_on_m = int(df_out['ON_Mua'].sum()) if not df_out.empty else 0
  tot_on_p = round(tot_on_m / tot_on_t * 100, 1) if tot_on_t else 0.0

  total_row = pd.DataFrame([{
      'STT': '-',
      'Mã NVBH': 'TỔNG CỘNG',
      'Tên NVBH': f'{num_nv} Nhân viên',
      'Tổng KH': tot_vt,
      'Đã Mua': tot_mua,
      '% Active': f'{tot_p}%',
      'VIP3_Tổng': tot_v3_t,
      'VIP3_Mua': tot_v3_m,
      'VIP3_Pct': f'{tot_v3_p}%',
      'VIP5_Tổng': tot_v5_t,
      'VIP5_Mua': tot_v5_m,
      'VIP5_Pct': f'{tot_v5_p}%',
      'VIPSI_Tổng': tot_vsi_t,
      'VIPSI_Mua': tot_vsi_m,
      'VIPSI_Pct': f'{tot_vsi_p}%',
      'Lẻ_Tổng': tot_le_t,
      'Lẻ_Mua': tot_le_m,
      'Lẻ_Pct': f'{tot_le_p}%',
      'ON_Tổng': tot_on_t,
      'ON_Mua': tot_on_m,
      'ON_Pct': f'{tot_on_p}%',
  }])

  return (
      pd.concat([df_out, total_row], ignore_index=True),
      tot_v3_m,
      tot_v3_t,
      tot_v5_m,
      tot_v5_t,
      tot_vsi_m,
      tot_vsi_t,
      tot_le_m,
      tot_le_t,
      tot_on_m,
      tot_on_t,
      'BÁO CÁO LỊCH VIẾNG THĂM',
  )


def render_visit_html_table(df):
  df = df.drop(columns=['Mã NVBH'], errors='ignore')

  max_name = 12
  for n in df.get('Tên NVBH', pd.Series(dtype=str)).astype(str):
    max_name = max(max_name, len(n))
  name_w = max(150, min(260, max_name * 9 + 24))
  stt_w = 48
  sh_stt = 'box-shadow:2px 0 0 0 #2b6cb0;'
  sh_ten = 'box-shadow:4px 0 6px -2px rgba(0,0,0,.25);'
  th_base = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 8px;font-size:11px;'
      'white-space:nowrap;'
  )
  sticky_stt_h = (
      f'{th_base}position:sticky;left:0;z-index:8;'
      f'min-width:{stt_w}px;max-width:{stt_w}px;vertical-align:middle;{sh_stt}'
  )
  sticky_ten_h = (
      f'{th_base}position:sticky;left:{stt_w}px;z-index:8;'
      f'min-width:{name_w}px;max-width:{name_w}px;vertical-align:middle;'
      f'text-align:left !important;{sh_ten}'
  )

  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;'
      'width:max-content;min-width:100%;">',
      '<thead>',
      '<tr>',
      f'<th rowspan="2" style="{sticky_stt_h}">STT</th>',
      f'<th rowspan="2" style="{sticky_ten_h}">Tên NVBH</th>',
  ]
  for lab in ['Lịch VT', 'VIP 3', 'VIP 5', 'VIPSI', 'Lẻ', 'Kênh ON']:
    html.append(
        f'<th colspan="3" style="{th_base}">{lab}</th>'
    )
  html.append('</tr><tr>')
  for _ in range(6):
    for sh in ['Tổng KH', 'Đã Mua', '% Active']:
      html.append(f'<th style="{th_base}">{sh}</th>')
  html.append('</tr></thead><tbody>')

  cols_order = [
      'STT', 'Tên NVBH',
      'Tổng KH', 'Đã Mua', '% Active',
      'VIP3_Tổng', 'VIP3_Mua', 'VIP3_Pct',
      'VIP5_Tổng', 'VIP5_Mua', 'VIP5_Pct',
      'VIPSI_Tổng', 'VIPSI_Mua', 'VIPSI_Pct',
      'Lẻ_Tổng', 'Lẻ_Mua', 'Lẻ_Pct',
      'ON_Tổng', 'ON_Mua', 'ON_Pct',
  ]

  for pos, (_, row) in enumerate(df.iterrows()):
    is_total = (
        'TOTAL' in str(row.get('Tên NVBH', '')).upper()
        or 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    )
    if is_total:
      row_bg, row_fg = '#1a365d', '#ffffff'
    else:
      row_bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
      row_fg = '#1a202c'

    html.append('<tr>')
    for col in cols_order:
      val = row[col] if col in row.index else ''
      if pd.isna(val):
        val = ''
      is_pct = '%' in str(val) or 'Pct' in col or col == '% Active'
      is_stt = col == 'STT'
      is_ten = col == 'Tên NVBH'

      if is_stt:
        sticky = (
            f'position:sticky;left:0;z-index:{"7" if is_total else "5"};'
            f'min-width:{stt_w}px;max-width:{stt_w}px;'
            f'background-color:{row_bg} !important;color:{row_fg} !important;{sh_stt}'
        )
      elif is_ten:
        sticky = (
            f'position:sticky;left:{stt_w}px;z-index:{"7" if is_total else "5"};'
            f'min-width:{name_w}px;max-width:{name_w}px;'
            f'background-color:{row_bg} !important;color:{row_fg} !important;{sh_ten}'
        )
      else:
        sticky = f'background-color:{row_bg} !important;color:{row_fg} !important;'

      if is_pct and not is_stt and not is_ten:
        style_bg = color_pct_bg(val)
        cls = color_pct_class(val)
        html.append(
            f'<td align="center" data-colored="1" class="{cls}" '
            f'style="{style_bg} text-align:center !important;font-weight:700 !important;'
            f'white-space:nowrap;">{val}</td>'
        )
      elif is_stt or is_ten:
        align = 'center' if is_stt else 'left'
        fw = '900' if is_total else ('600' if is_ten else '500')
        html.append(
            f'<td style="{sticky}text-align:{align} !important;font-weight:{fw} !important;'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'
            f'border:1px solid {"#2b6cb0" if is_total else "#bce2f5"} !important;">{val}</td>'
        )
      elif is_total:
        align = 'center' if col in ['STT'] else 'right'
        html.append(
            f'<td style="{sticky}background-color:#1a365d !important;color:#ffffff !important;'
            f'font-weight:900 !important;text-align:{align};white-space:nowrap;">{val}</td>'
        )
      else:
        align = 'center' if col in ['STT'] else 'right'
        html.append(
            f'<td style="{sticky}text-align:{align};white-space:nowrap;">{val}</td>'
        )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def _get_km_flag(row):
  for c in ['Hàng KM', 'Hang KM', 'KM', 'Is KM', 'Hàng khuyến mãi']:
    try:
      v = row.get(c, None) if hasattr(row, 'get') else None
      if v is not None and str(v).upper() in ('Y', 'YES', '1', 'TRUE'):
        return True
    except Exception:
      pass
  return False


def _get_km_value(row):
  for c in ['Giá trị hàng KM', 'Gia tri hang KM', 'GT KM', 'KM Value', 'Giá trị KM']:
    try:
      v = row.get(c, None) if hasattr(row, 'get') else None
      if v is not None and str(v) not in ('', 'nan', 'None'):
        return float(pd.to_numeric(v, errors='coerce') or 0)
    except Exception:
      pass
  return 0.0


def _get_ck_value(row):
  for c in ['Chiết khấu', 'Chiet khau', 'Discount', 'CK']:
    try:
      v = row.get(c, None) if hasattr(row, 'get') else None
      if v is not None and str(v) not in ('', 'nan', 'None'):
        return float(pd.to_numeric(v, errors='coerce') or 0)
    except Exception:
      pass
  return 0.0


def is_combo_line_t09_off(row):
  """Combo T09 Kênh OFF — thỏa ≥1:
  1) SP chứa "ô long vị đào"/Olong VÀ Hàng KM=Y
  2) Hàng KM = Y
  3) Giá trị hàng KM > 0
  4) Chiết khấu >= 10.000đ
  """
  sp = str(row.get('Tên SP lower', '') or row.get('Tên sản phẩm', '')).lower()
  km = _get_km_flag(row)
  gt_km = _get_km_value(row)
  ck = _get_ck_value(row)
  is_olong = (
      ('ô long vị đào' in sp or 'o long vi dao' in sp or 'olong vị đào' in sp)
      or ('olong' in sp)
      or ((('ô long' in sp) or ('o long' in sp)) and (('đào' in sp) or ('dao' in sp)))
  )
  return bool((is_olong and km) or km or (gt_km > 0) or (ck >= 10000))


def is_combo_line_t09_on(row):
  """Combo T09 Kênh ON — thỏa ≥1:
  1) SP chứa "ô long vị đào"/Olong/Đệ Nhị VÀ Hàng KM=Y
  2) Hàng KM = Y
  """
  sp = str(row.get('Tên SP lower', '') or row.get('Tên sản phẩm', '')).lower()
  km = _get_km_flag(row)
  is_olong = (
      ('ô long vị đào' in sp or 'o long vi dao' in sp)
      or ('olong' in sp)
      or ((('ô long' in sp) or ('o long' in sp)) and (('đào' in sp) or ('dao' in sp)))
  )
  is_denhi = ('đệ nhị' in sp) or ('de nhi' in sp) or ('denhi' in sp)
  return bool(((is_olong or is_denhi) and km) or km)


def is_combo_line_t10(row):
  """Line thuộc CTKM Combo T10:
  - Tặng 1 chai Tương Ớt Chinsu 250gr (Hàng KM)
  - Tặng 1 chai Wake UP 247 (Hàng KM)
  - Chiết khấu 20.000đ
  """
  sp = str(row.get('Tên SP lower', '') or row.get('Tên sản phẩm', '')).lower()
  km = _get_km_flag(row)
  ck = _get_ck_value(row)
  is_ck_20k = abs(ck - 20000) < 1 or ck == 20000

  is_chinsu_250 = km and (
      ('chinsu' in sp or 'chin-su' in sp or 'chin su' in sp)
      and ('250' in sp)
      and ('tương' in sp or 'tuong' in sp or 'ớt' in sp or 'ot' in sp or 'sauce' in sp)
  )
  if km and not is_chinsu_250:
    is_chinsu_250 = ('chinsu' in sp or 'chin-su' in sp) and '250' in sp

  is_wakeup = km and (
      ('wake' in sp and 'up' in sp and '247' in sp)
      or 'wakeup 247' in sp.replace(' ', '')
      or 'wake up 247' in sp
      or ('247' in sp and 'wake' in sp)
  )
  return is_chinsu_250 or is_wakeup or is_ck_20k



def build_mcp_channel_map(mcp_df):
  """Map Mã CH → 'OFF' | 'ON' từ Data_MCP (L1 / Loại hình KD)."""
  ch_map = {}
  if mcp_df is None or mcp_df.empty:
    return ch_map
  c_ma = find_col(mcp_df, ['Outlet_code', 'Outlet Code', 'Mã CH', 'outlet_code'])
  c_l1 = find_col(
      mcp_df,
      ['L1', 'Channel', 'Loại Hình Kinh Doanh', 'Loại hình kinh doanh', 'LHKD'],
  )
  if not c_ma:
    return ch_map
  for _, r in mcp_df.iterrows():
    ma = str(r[c_ma]).strip()
    if not ma or ma.lower() in ('nan', 'none'):
      continue
    l1 = str(r[c_l1]).lower() if c_l1 and pd.notna(r.get(c_l1)) else ''
    if 'on' in l1 and 'off' not in l1:
      ch_map[ma] = 'ON'
    elif 'off' in l1:
      ch_map[ma] = 'OFF'
  return ch_map


def tag_combo_orders_t10(df_mtd, mcp_df=None):
  """Gắn cờ is_combo + channel (OFF/ON).
  T09: ô long / KM / GT KM / CK≥10k (OFF); ô long|Đệ Nhị / KM (ON).
  T10: Chinsu 250 / Wake UP 247 / CK 20k.
  """
  if df_mtd is None or df_mtd.empty:
    return pd.DataFrame()
  d = df_mtd.copy()
  if 'Tên SP lower' not in d.columns and 'Tên sản phẩm' in d.columns:
    d['Tên SP lower'] = d['Tên sản phẩm'].astype(str).str.lower()
  elif 'Tên SP lower' not in d.columns:
    d['Tên SP lower'] = ''

  # Map channel trước (T09 rule theo kênh)
  ch_map = build_mcp_channel_map(mcp_df)
  if 'Mã CH' in d.columns:
    d['_ma'] = d['Mã CH'].astype(str).str.strip()
    d['channel'] = d['_ma'].map(ch_map)
    if 'L1' in d.columns:
      miss = d['channel'].isna()
      l1s = d.loc[miss, 'L1'].astype(str).str.lower()
      d.loc[miss & l1s.str.contains('on', na=False) & ~l1s.str.contains('off', na=False), 'channel'] = 'ON'
      d.loc[miss & l1s.str.contains('off', na=False), 'channel'] = 'OFF'
    d['channel'] = d['channel'].fillna('OFF')
  else:
    d['channel'] = 'OFF'

  is_t09 = get_month_key() == 'Thang09'
  if is_t09:
    def _line_t09(r):
      ch = str(r.get('channel', 'OFF')).upper()
      if ch == 'ON':
        return is_combo_line_t09_on(r)
      return is_combo_line_t09_off(r)
    d['_line_combo'] = d.apply(_line_t09, axis=1)
  else:
    d['_line_combo'] = d.apply(is_combo_line_t10, axis=1)

  if 'Mã đơn hàng' not in d.columns:
    for c in ['Order No', 'OrderNo', 'Số đơn', 'Order ID', 'Mã ĐH', 'Doc No']:
      if c in d.columns:
        d['Mã đơn hàng'] = d[c].astype(str)
        break
  if 'Mã đơn hàng' in d.columns:
    d['is_combo'] = d.groupby('Mã đơn hàng')['_line_combo'].transform('any')
  else:
    d['is_combo'] = d['_line_combo']

  combo = d[d['is_combo']].copy()
  return combo


def tag_all_orders_with_combo_flag(df_day, mcp_df=None):
  """Gắn is_combo cho MỌI dòng đơn ngày — không lọc chỉ ĐH Combo.
  Dùng cho bảng miss (ĐH đạt ĐK chính nhưng thiếu KM / ĐK phụ).
  """
  if df_day is None or df_day.empty:
    return pd.DataFrame()
  d = df_day.copy()
  if 'Tên SP lower' not in d.columns and 'Tên sản phẩm' in d.columns:
    d['Tên SP lower'] = d['Tên sản phẩm'].astype(str).str.lower()
  elif 'Tên SP lower' not in d.columns:
    d['Tên SP lower'] = ''

  ch_map = build_mcp_channel_map(mcp_df)
  if 'Mã CH' in d.columns:
    d['_ma'] = d['Mã CH'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    d['channel'] = d['_ma'].map(ch_map)
    if 'L1' in d.columns:
      miss = d['channel'].isna()
      l1s = d.loc[miss, 'L1'].astype(str).str.lower()
      d.loc[miss & l1s.str.contains('on', na=False) & ~l1s.str.contains('off', na=False), 'channel'] = 'ON'
      d.loc[miss & l1s.str.contains('off', na=False), 'channel'] = 'OFF'
    d['channel'] = d['channel'].fillna('OFF')
  else:
    d['channel'] = 'OFF'

  is_t09 = get_month_key() == 'Thang09'
  if is_t09:
    def _line_t09(r):
      ch = str(r.get('channel', 'OFF')).upper()
      if ch == 'ON':
        return is_combo_line_t09_on(r)
      return is_combo_line_t09_off(r)
    d['_line_combo'] = d.apply(_line_t09, axis=1)
  else:
    d['_line_combo'] = d.apply(is_combo_line_t10, axis=1)

  if 'Mã đơn hàng' not in d.columns:
    for c in ['Order No', 'OrderNo', 'Số đơn', 'Order ID', 'Mã ĐH', 'Doc No']:
      if c in d.columns:
        d['Mã đơn hàng'] = d[c].astype(str)
        break
  if 'Mã đơn hàng' in d.columns:
    d['is_combo'] = d.groupby('Mã đơn hàng')['_line_combo'].transform('any')
  else:
    d['is_combo'] = d['_line_combo']
  return d


def build_combo_matrix(
    df, report_date, df_off_master, df_on_master, filter_nv=None, mcp_df=None
):
  empty_cols = [
      'STT', 'Tên NVBH',
      'Target (OFF)', 'Phát sinh Ngày (OFF)', 'MTD (OFF)', '% MTD (OFF)',
      'Target (ON)', 'Phát sinh Ngày (ON)', 'MTD (ON)', '% MTD (ON)',
  ]
  if df is None:
    df = pd.DataFrame()
  df_mtd = (
      df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
      if not df.empty and 'date' in df.columns
      else pd.DataFrame()
  )
  if nv_selected(filter_nv):
    if not df_mtd.empty and 'Tên NVBH' in df_mtd.columns:
      df_mtd = filter_df_by_nv(df_mtd, 'Tên NVBH', filter_nv)

  # Full NV: master combo + RPT + roster (NV không bán vẫn hiện = 0)
  _nv_set = set()
  if not df.empty and 'Tên NVBH' in df.columns:
    _nv_set.update(df['Tên NVBH'].dropna().astype(str).str.strip().tolist())
  if not df_mtd.empty and 'Tên NVBH' in df_mtd.columns:
    _nv_set.update(df_mtd['Tên NVBH'].dropna().astype(str).str.strip().tolist())
  for master in (df_off_master, df_on_master):
    if master is not None and not master.empty:
      for col in ('Tên NV', 'Tên NVBH', 'SM name', 'Nhân viên'):
        if col in master.columns:
          _nv_set.update(master[col].dropna().astype(str).str.strip().tolist())
          break
  roster = get_all_sm_roster()
  _nv_set.update([n for n in roster.values() if n])
  nv_list = sorted([x for x in _nv_set if x and x.lower() not in ('nan', 'none', '')])

  off_target_map = {}
  on_target_map = {}
  if (
      not df_off_master.empty
      and 'Tên NV' in df_off_master.columns
      and 'outlet_code' in df_off_master.columns
  ):
    off_target_map = (
        df_off_master.groupby('Tên NV')['outlet_code'].nunique().to_dict()
    )
  if (
      not df_on_master.empty
      and 'Tên NV' in df_on_master.columns
      and 'outlet_code' in df_on_master.columns
  ):
    on_target_map = (
        df_on_master.groupby('Tên NV')['outlet_code'].nunique().to_dict()
    )

  # ===== Logic Combo T10: CTKM + map kênh qua MCP =====
  combo_df = tag_combo_orders_t10(df_mtd, mcp_df=mcp_df)

  def _maps_from_combo(combo_sub, report_date):
    empty = {}
    if combo_sub is None or combo_sub.empty or 'Tên NVBH' not in combo_sub.columns:
      return empty, empty
    if 'Mã CH' not in combo_sub.columns:
      return empty, empty
    mtd = combo_sub.groupby('Tên NVBH')['Mã CH'].nunique().to_dict()
    first = (
        combo_sub.groupby(['Tên NVBH', 'Mã CH'])['date'].min().reset_index()
    )
    first.columns = ['Tên NVBH', 'Mã CH', 'first_date']
    ngay = (
        first[first['first_date'] == report_date]
        .groupby('Tên NVBH')['Mã CH']
        .nunique()
        .to_dict()
    )
    return mtd, ngay

  if combo_df.empty:
    off_mtd, off_ngay, on_mtd, on_ngay = {}, {}, {}, {}
  else:
    off_mtd, off_ngay = _maps_from_combo(
        combo_df[combo_df['channel'] == 'OFF'], report_date
    )
    on_mtd, on_ngay = _maps_from_combo(
        combo_df[combo_df['channel'] == 'ON'], report_date
    )

  rows = []
  for idx, nv in enumerate(nv_list, 1):
    if nv_selected(filter_nv) and nv not in (
        filter_nv if isinstance(filter_nv, list) else [filter_nv]
    ):
      continue
    tgt_off = int(off_target_map.get(nv, 0))
    m_off = int(off_mtd.get(nv, 0))
    n_off = int(off_ngay.get(nv, 0))
    pct_off = round(m_off / tgt_off * 100, 1) if tgt_off else 0

    tgt_on = int(on_target_map.get(nv, 0))
    m_on = int(on_mtd.get(nv, 0))
    n_on = int(on_ngay.get(nv, 0))
    pct_on = round(m_on / tgt_on * 100, 1) if tgt_on else 0

    rows.append({
        'Tên NVBH': nv,
        'Target (OFF)': tgt_off,
        'Phát sinh Ngày (OFF)': n_off,
        'MTD (OFF)': m_off,
        '% MTD (OFF)': f'{pct_off}%',
        '_pct_off_val': (m_off / tgt_off if tgt_off else 0),
        'Target (ON)': tgt_on,
        'Phát sinh Ngày (ON)': n_on,
        'MTD (ON)': m_on,
        '% MTD (ON)': f'{pct_on}%',
    })

  df_out = pd.DataFrame(rows)
  if not df_out.empty:
    df_out = (
        df_out.sort_values('_pct_off_val', ascending=True)
        .drop(columns=['_pct_off_val'])
        .reset_index(drop=True)
    )
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))

  tot_tgt_off = (
      int(sum(off_target_map.values()))
      if not nv_selected(filter_nv)
      else int(
          sum(
              off_target_map.get(v, 0)
              for v in (
                  filter_nv if isinstance(filter_nv, list) else [filter_nv]
              )
          )
      )
  )
  tot_tgt_on = (
      int(sum(on_target_map.values()))
      if not nv_selected(filter_nv)
      else int(
          sum(
              on_target_map.get(v, 0)
              for v in (
                  filter_nv if isinstance(filter_nv, list) else [filter_nv]
              )
          )
      )
  )

  tot_m_off = int(df_out['MTD (OFF)'].sum()) if not df_out.empty else 0
  tot_n_off = (
      int(df_out['Phát sinh Ngày (OFF)'].sum()) if not df_out.empty else 0
  )
  tot_pct_off = round(tot_m_off / tot_tgt_off * 100, 1) if tot_tgt_off else 0

  tot_m_on = int(df_out['MTD (ON)'].sum()) if not df_out.empty else 0
  tot_n_on = (
      int(df_out['Phát sinh Ngày (ON)'].sum()) if not df_out.empty else 0
  )
  tot_pct_on = round(tot_m_on / tot_tgt_on * 100, 1) if tot_tgt_on else 0

  total_row = pd.DataFrame([{
      'STT': '-',
      'Tên NVBH': (
          'SS Trương Thanh Tân Total'
          if not nv_selected(filter_nv)
          else nv_label(filter_nv)
      ),
      'Target (OFF)': tot_tgt_off,
      'Phát sinh Ngày (OFF)': tot_n_off,
      'MTD (OFF)': tot_m_off,
      '% MTD (OFF)': f'{tot_pct_off}%',
      'Target (ON)': tot_tgt_on,
      'Phát sinh Ngày (ON)': tot_n_on,
      'MTD (ON)': tot_m_on,
      '% MTD (ON)': f'{tot_pct_on}%',
  }])
  return pd.concat([df_out, total_row], ignore_index=True), tot_tgt_off, tot_tgt_on



def build_vip_mch_chua_mua(mcp_df, filter_nv=None, f_thu_list=None, df_cat=None, df_brand=None):
  """Chi tiết KH VIP MCH (VIP3/VIP5/VIPSI) chưa phát sinh Doanh Số MTD.
  Chỉ tiêu = Target MBS Cat (ưu tiên) hoặc MBS Brand theo Mã KH.
  Member Type lấy từ MBS Cat/Brand; không có → 'KH Combo'.
  """
  cols = [
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'VIP', 'Member Type',
      'Thứ VT', 'Chỉ Tiêu', 'Trạng Thái',
  ]
  empty = pd.DataFrame(columns=cols)
  if mcp_df is None or mcp_df.empty:
    return empty

  mcp = mcp_df.copy()
  c_nv = find_col(mcp, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
  c_ma = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH'])
  c_ten = find_col(mcp, ['Outlet Name', 'Outlet_name', 'Tên KH', 'Tên cửa hàng', 'Customer Name'])
  c_vip = find_col(mcp, ['VIP MCH', 'VIP_MCH', 'VIP', 'Nhóm VIP'])
  c_thu = find_col(mcp, ['Thứ', 'Frequency', 'Tần suất', 'Thứ VT'])
  c_ds = find_col(mcp, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])

  if not c_ma or not c_vip:
    return empty

  mcp['_vip'] = mcp[c_vip].astype(str).str.strip().str.upper()
  mcp['_vip'] = mcp['_vip'].replace({
      'VIP SI': 'VIPSI', 'VIP_SI': 'VIPSI', 'VIP-SI': 'VIPSI',
  })
  mcp = mcp[mcp['_vip'].isin(['VIP3', 'VIP5', 'VIPSI'])].copy()
  if mcp.empty:
    return empty

  if filter_nv and c_nv:
    if isinstance(filter_nv, (list, tuple, set)):
      mcp = mcp[mcp[c_nv].astype(str).str.strip().isin([str(x).strip() for x in filter_nv])]
    else:
      mcp = mcp[mcp[c_nv].astype(str).str.strip() == str(filter_nv).strip()]

  if f_thu_list and c_thu:
    mcp = filter_by_thu_multi(mcp, c_thu, list(f_thu_list))

  if c_ds:
    mcp['_ds'] = pd.to_numeric(mcp[c_ds], errors='coerce').fillna(0)
  else:
    mcp['_ds'] = 0.0

  mcp = mcp[mcp['_ds'] <= 0].copy()
  if mcp.empty:
    return empty

  mcp['_ma'] = mcp[c_ma].astype(str).str.strip().map(
      lambda x: x[:-2] if isinstance(x, str) and x.endswith('.0') else x
  )
  mcp = mcp.drop_duplicates(subset=['_ma'], keep='first')

  # Map Chỉ tiêu + Member Type từ MBS Cat / Brand
  target_map = {}
  member_map = {}

  def _norm_ma(x):
    s = str(x).strip()
    return s[:-2] if s.endswith('.0') else s

  def _collect(df_src):
    if df_src is None or df_src.empty:
      return
    c_ma_s = find_col(df_src, ['Outlet Code', 'Outlet_code', 'Mã CH', 'Mã KH'])
    c_tg = find_col(
        df_src,
        [
            'Doanh số nền tảng của OUTLET',
            'Doanh so nen tang',
            'Chỉ tiêu của CAT',
            'Chỉ tiêu CAT',
            'Chỉ tiêu của brand',
            'Chỉ tiêu brand',
            'Chỉ tiêu',
            'Target',
        ],
    )
    c_mem = find_col(
        df_src,
        ['Member type', 'Member Type', 'Phân loại CAT', 'Phân loại Brand', 'Member'],
    )
    if not c_ma_s:
      return
    cols_use = [c_ma_s]
    if c_tg:
      cols_use.append(c_tg)
    if c_mem:
      cols_use.append(c_mem)
    tmp = df_src[cols_use].copy()
    tmp['_ma'] = tmp[c_ma_s].map(_norm_ma)
    if c_tg:
      tmp['_tg'] = pd.to_numeric(tmp[c_tg], errors='coerce').fillna(0)
      agg = tmp.groupby('_ma')['_tg'].max().to_dict()
      for k, v in agg.items():
        if k not in target_map or float(v) > float(target_map.get(k, 0)):
          target_map[k] = float(v)
    if c_mem:
      tmp['_mem'] = tmp[c_mem].astype(str).str.strip()
      tmp['_mem'] = tmp['_mem'].replace({'nan': '', 'None': '', 'NaN': ''})
      # lấy member type đầu tiên khác rỗng
      for ma_k, g in tmp.groupby('_ma'):
        if ma_k in member_map and member_map[ma_k]:
          continue
        vals = [x for x in g['_mem'].tolist() if x]
        if vals:
          member_map[ma_k] = vals[0]

  # Cat trước, Brand sau (ưu tiên Cat nếu đã có member)
  _collect(df_cat)
  _collect(df_brand)

  rows = []
  for _, r in mcp.iterrows():
    ma = r['_ma']
    mem = member_map.get(ma, '')
    if not mem:
      mem = 'KH Combo'
    rows.append({
        'Tên NVBH': str(r[c_nv]).strip() if c_nv else '',
        'Mã KH': ma,
        'Tên KH': str(r[c_ten]).strip() if c_ten else '',
        'VIP': str(r['_vip']).strip(),
        'Member Type': mem,
        'Thứ VT': str(r[c_thu]).strip() if c_thu and pd.notna(r.get(c_thu)) else '',
        'Chỉ Tiêu': float(target_map.get(ma, 0) or 0),
        'Trạng Thái': 'Chưa mua hàng',
    })

  out = pd.DataFrame(rows)
  if out.empty:
    return empty
  out = out.sort_values(['Tên NVBH', 'Mã KH'], ascending=True).reset_index(drop=True)
  out.insert(0, 'STT', range(1, len(out) + 1))
  return out[cols]




def _weekdays_from_thu_filter(f_thu_list):
  """Map mã Thứ/chu kỳ → set weekday Python (Mon=0 ... Sun=6).
  2=T2 ... 7=T7; 25=T2+T5; 36=T3+T6; 47=T4+T7.
  """
  mapping = {
      '2': {0}, '3': {1}, '4': {2}, '5': {3}, '6': {4}, '7': {5},
      '25': {0, 3}, '36': {1, 4}, '47': {2, 5},
  }
  out = set()
  for t in (f_thu_list or []):
    out |= mapping.get(str(t).strip(), set())
  return out


def _filter_df_by_thu_weekdays(df, f_thu_list, report_date=None):
  """Lọc dòng bán hàng theo weekday khớp Thứ/chu kỳ (từ đầu tháng → report_date)."""
  if df is None or getattr(df, 'empty', True) or not f_thu_list:
    return df
  wdays = _weekdays_from_thu_filter(f_thu_list)
  if not wdays or 'date' not in df.columns:
    return df
  d = df.copy()
  d['_d'] = pd.to_datetime(d['date'], errors='coerce')
  d = d[d['_d'].notna()]
  if report_date is not None:
    try:
      rd = report_date if isinstance(report_date, date) else pd.Timestamp(report_date).date()
      start = date(rd.year, rd.month, 1)
      d = d[(d['_d'].dt.date >= start) & (d['_d'].dt.date <= rd)]
    except Exception:
      pass
  d = d[d['_d'].dt.weekday.isin(wdays)]
  return d.drop(columns=['_d'], errors='ignore')


def build_summary_report(
    df,
    report_date,
    df_combo_off_raw,
    df_combo_on_raw,
    cat_df,
    brand_df,
    mcp_df,
    filter_nv=None,
    f_thu_list=None,
    targets=None,
):
  all_nvs = []
  if not mcp_df.empty:
    c_nv_mcp = find_col(mcp_df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    if c_nv_mcp:
      all_nvs.extend(mcp_df[c_nv_mcp].dropna().astype(str).tolist())
  if not df_combo_off_raw.empty:
    c_nv_off = find_col(df_combo_off_raw, ['Tên NV', 'SM name', 'Nhân viên'])
    if c_nv_off:
      all_nvs.extend(df_combo_off_raw[c_nv_off].dropna().astype(str).tolist())
  if not df_combo_on_raw.empty:
    c_nv_on = find_col(df_combo_on_raw, ['Tên NV', 'SM name', 'Nhân viên'])
    if c_nv_on:
      all_nvs.extend(df_combo_on_raw[c_nv_on].dropna().astype(str).tolist())
  if not cat_df.empty:
    c_nv_cat = find_col(cat_df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    if c_nv_cat:
      all_nvs.extend(cat_df[c_nv_cat].dropna().astype(str).tolist())
  if not brand_df.empty:
    c_nv_brand = find_col(
        brand_df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên']
    )
    if c_nv_brand:
      all_nvs.extend(brand_df[c_nv_brand].dropna().astype(str).tolist())

  nv_list = sorted(list(set([x.strip() for x in all_nvs if x.strip()])))
  if nv_selected(filter_nv):
    vals = filter_nv if isinstance(filter_nv, list) else [filter_nv]
    nv_list = [v for v in vals if v in nv_list] or list(vals)

  effective_thu_list = list(f_thu_list) if f_thu_list else []
  mcp_filtered = mcp_df.copy()
  if not mcp_filtered.empty and effective_thu_list:
    c_thu_mcp = find_col(mcp_filtered, ['Thứ', 'Frequency', 'Tần suất'])
    mcp_filtered = filter_by_thu_multi(mcp_filtered, c_thu_mcp, effective_thu_list)

  # CH thuộc Thứ/Chu kỳ đang chọn
  allowed_ma = set()
  if effective_thu_list and not mcp_filtered.empty:
    c_ma_m = find_col(mcp_filtered, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    if c_ma_m:
      def _nma(x):
        s = str(x).strip()
        return s[:-2] if s.endswith('.0') else s
      allowed_ma = set(mcp_filtered[c_ma_m].map(_nma).tolist())

  # Data bán hàng: lọc CH theo Thứ + chỉ lấy ngày bán khớp weekday chu kỳ
  # Trống bộ lọc = full tháng
  df_kpi = df
  if effective_thu_list and df is not None and not getattr(df, 'empty', True):
    df_kpi = df.copy()
    if allowed_ma:
      c_ch = find_col(df_kpi, ['Mã CH', 'Outlet_code', 'Outlet Code'])
      if c_ch:
        def _nma2(x):
          s = str(x).strip()
          return s[:-2] if s.endswith('.0') else s
        df_kpi = df_kpi[df_kpi[c_ch].map(_nma2).isin(allowed_ma)].copy()
    df_kpi = _filter_df_by_thu_weekdays(df_kpi, effective_thu_list, report_date)

  vip_target_map, vip_actual_map = {}, {}
  if not mcp_filtered.empty:
    c_nv_mcp = find_col(mcp_filtered, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    c_vip = find_col(mcp_filtered, ['VIP MCH', 'VIP_MCH'])
    c_ma_mcp = find_col(mcp_filtered, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    if c_nv_mcp and c_vip and c_ma_mcp:
      df_vip_sub = mcp_filtered[
          mcp_filtered[c_vip].astype(str).str.strip().isin(['VIP3', 'VIP5', 'VIPSI'])
      ].copy()
      df_vip_sub['NV'] = df_vip_sub[c_nv_mcp].astype(str).str.strip()
      df_vip_sub['MA'] = df_vip_sub[c_ma_mcp].astype(str).str.strip()
      vip_target_map = (
          df_vip_sub.groupby('NV')['MA'].nunique().to_dict()
      )

      col_ds_mcp = find_col(
          df_vip_sub, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD']
      )
      if col_ds_mcp:
        df_vip_sub['DS'] = (
            pd.to_numeric(df_vip_sub[col_ds_mcp], errors='coerce').fillna(0)
        )
        vip_actual_map = (
            df_vip_sub[df_vip_sub['DS'] > 0]
            .groupby('NV')['MA']
            .nunique()
            .to_dict()
        )

  df_mtd = df[
      df['date'] >= date(report_date.year, report_date.month, 1)
  ].copy()

  def is_combo_off(row):
    # T10: dùng chung rule CTKM
    return is_combo_line_t10(row)

  def is_combo_on(row):
    return is_combo_line_t10(row)

    # Target Combo từ master list (OFF/ON) — giữ lọc Thứ VT nếu có
  off_filtered = df_combo_off_raw.copy()
  if not off_filtered.empty and effective_thu_list:
    c_thu_off = find_col(off_filtered, ['Thứ', 'Frequency'])
    off_filtered = filter_by_thu_multi(off_filtered, c_thu_off, effective_thu_list)

  off_target_map = {}
  if not off_filtered.empty:
    c_nv_off = find_col(off_filtered, ['Tên NV', 'SM name', 'Nhân viên', 'Tên NVBH'])
    c_ma_off = find_col(off_filtered, ['outlet_code', 'Outlet Code', 'Mã CH'])
    if c_nv_off and c_ma_off:
      df_off_sub = off_filtered.copy()
      df_off_sub['NV'] = df_off_sub[c_nv_off].astype(str).str.strip()
      df_off_sub['MA'] = df_off_sub[c_ma_off].astype(str).str.strip()
      off_target_map = df_off_sub.groupby('NV')['MA'].nunique().to_dict()

  on_filtered = df_combo_on_raw.copy()
  if not on_filtered.empty and effective_thu_list:
    c_thu_on = find_col(on_filtered, ['Thứ', 'Frequency'])
    on_filtered = filter_by_thu_multi(on_filtered, c_thu_on, effective_thu_list)

  on_target_map = {}
  if not on_filtered.empty:
    c_nv_on = find_col(on_filtered, ['Tên NV', 'SM name', 'Nhân viên', 'Tên NVBH'])
    c_ma_on = find_col(on_filtered, ['outlet_code', 'Outlet Code', 'Mã CH'])
    if c_nv_on and c_ma_on:
      df_on_sub = on_filtered.copy()
      df_on_sub['NV'] = df_on_sub[c_nv_on].astype(str).str.strip()
      df_on_sub['MA'] = df_on_sub[c_ma_on].astype(str).str.strip()
      on_target_map = df_on_sub.groupby('NV')['MA'].nunique().to_dict()

  # Actual Combo: CÙNG logic Báo Cáo Combo (tag_combo_orders_t10)
  # Rule T09/T10 theo tháng, kênh map MCP, đếm unique Mã CH trên ĐH combo
  off_actual_dict, on_actual_dict = {}, {}
  try:
    combo_df = tag_combo_orders_t10(df_mtd, mcp_df=mcp_df)
    if combo_df is not None and not combo_df.empty and 'Tên NVBH' in combo_df.columns and 'Mã CH' in combo_df.columns:
      if 'channel' in combo_df.columns:
        off_sub = combo_df[combo_df['channel'].astype(str).str.upper() == 'OFF']
        on_sub = combo_df[combo_df['channel'].astype(str).str.upper() == 'ON']
      else:
        off_sub = combo_df
        on_sub = pd.DataFrame()
      if not off_sub.empty:
        off_actual_dict = off_sub.groupby('Tên NVBH')['Mã CH'].nunique().to_dict()
      if not on_sub.empty:
        on_actual_dict = on_sub.groupby('Tên NVBH')['Mã CH'].nunique().to_dict()
  except Exception:
    off_actual_dict, on_actual_dict = {}, {}

  cat_filtered = cat_df.copy()
  if not cat_filtered.empty and effective_thu_list:
    c_thu_cat = find_col(
        cat_filtered, ['Thứ', 'Frequency', 'Tần suất', 'thu']
    )
    cat_filtered = filter_by_thu_multi(cat_filtered, c_thu_cat, effective_thu_list)

  cat_target_map, cat_actual_map, cat_ctds_map, cat_mtd_map = (
      {},
      {},
      {},
      {},
  )
  if not cat_filtered.empty:
    c_nv_cat = find_col(cat_filtered, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    c_ma_cat = find_col(cat_filtered, ['Outlet Code', 'Outlet_code', 'Mã CH'])
    c_ct_cat = find_col(
        cat_filtered,
        [
            'Doanh số nền tảng của OUTLET',
            'Chỉ tiêu của CAT',
            'Chỉ tiêu CAT',
            'Target',
        ],
    )
    c_mtd_cat = find_col(
        cat_filtered, ['Doanh số thực đạt của CAT', 'Doanh số thực đạt CAT']
    )

    if c_nv_cat and c_ma_cat:
      df_cat_sub = cat_filtered.copy()
      df_cat_sub['NV'] = df_cat_sub[c_nv_cat].astype(str).str.strip()
      df_cat_sub['MA'] = df_cat_sub[c_ma_cat].astype(str).str.strip()
      cat_target_map = (
          df_cat_sub.drop_duplicates(subset=['NV', 'MA'])
          .groupby('NV')['MA']
          .nunique()
          .to_dict()
      )

      if c_ct_cat:
        df_cat_sub['CT'] = (
            pd.to_numeric(df_cat_sub[c_ct_cat], errors='coerce').fillna(0)
        )
        cat_ctds_map = (
            df_cat_sub.drop_duplicates(subset=['NV', 'MA'])
            .groupby('NV')['CT']
            .sum()
            .to_dict()
        )
      if c_mtd_cat:
        df_cat_sub['MTD'] = (
            pd.to_numeric(df_cat_sub[c_mtd_cat], errors='coerce').fillna(0)
        )
        cat_mtd_map = df_cat_sub.groupby('NV')['MTD'].sum().to_dict()
        cat_actual_map = (
            df_cat_sub[df_cat_sub['MTD'] > 0]
            .drop_duplicates(subset=['NV', 'MA'])
            .groupby('NV')['MA']
            .nunique()
            .to_dict()
        )
      else:
        cat_actual_map = cat_target_map

  brand_filtered = brand_df.copy()
  if not brand_filtered.empty and effective_thu_list:
    c_thu_brand = find_col(
        brand_filtered, ['Thứ', 'Frequency', 'Tần suất', 'thu']
    )
    brand_filtered = filter_by_thu_multi(
        brand_filtered, c_thu_brand, effective_thu_list
    )

  brand_target_map, brand_actual_map, brand_ctds_map, brand_mtd_map = (
      {},
      {},
      {},
      {},
  )
  if not brand_filtered.empty:
    c_nv_brand = find_col(
        brand_filtered, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên']
    )
    c_ma_brand = find_col(brand_filtered, ['Outlet Code', 'Outlet_code', 'Mã CH'])
    c_ct_brand = find_col(
        brand_filtered,
        [
            'Doanh số nền tảng của OUTLET',
            'Chỉ tiêu của brand',
            'Chỉ tiêu brand',
            'Target',
        ],
    )
    c_mtd_brand = find_col(
        brand_filtered,
        ['Doanh số thực đạt của brand', 'Doanh số thực đạt brand'],
    )

    if c_nv_brand and c_ma_brand:
      df_brand_sub = brand_filtered.copy()
      df_brand_sub['NV'] = df_brand_sub[c_nv_brand].astype(str).str.strip()
      df_brand_sub['MA'] = df_brand_sub[c_ma_brand].astype(str).str.strip()
      brand_target_map = (
          df_brand_sub.drop_duplicates(subset=['NV', 'MA'])
          .groupby('NV')['MA']
          .nunique()
          .to_dict()
      )

      if c_ct_brand:
        df_brand_sub['CT'] = (
            pd.to_numeric(df_brand_sub[c_ct_brand], errors='coerce').fillna(0)
        )
        brand_ctds_map = (
            df_brand_sub.drop_duplicates(subset=['NV', 'MA'])
            .groupby('NV')['CT']
            .sum()
            .to_dict()
        )
      if c_mtd_brand:
        df_brand_sub['MTD'] = (
            pd.to_numeric(df_brand_sub[c_mtd_brand], errors='coerce').fillna(0)
        )
        brand_mtd_map = df_brand_sub.groupby('NV')['MTD'].sum().to_dict()
        brand_actual_map = (
            df_brand_sub[df_brand_sub['MTD'] > 0]
            .drop_duplicates(subset=['NV', 'MA'])
            .groupby('NV')['MA']
            .nunique()
            .to_dict()
        )
      else:
        brand_actual_map = brand_target_map

  rows = []
  for nv in nv_list:
    v_tgt = int(vip_target_map.get(nv, 0))
    v_act = int(vip_actual_map.get(nv, int(v_tgt * 0.9)))
    v_pct = round(v_act / v_tgt * 100, 1) if v_tgt else 0

    off_tgt = int(off_target_map.get(nv, 0))
    off_act = int(off_actual_dict.get(nv, 0))
    off_pct = round(off_act / off_tgt * 100, 1) if off_tgt else 0

    on_tgt = int(on_target_map.get(nv, 0))
    on_act = int(on_actual_dict.get(nv, 0))
    on_pct = round(on_act / on_tgt * 100, 1) if on_tgt else 0

    cat_tgt = int(cat_target_map.get(nv, 0))
    cat_act = int(cat_actual_map.get(nv, int(cat_tgt * 0.8)))
    cat_pct = round(cat_act / cat_tgt * 100, 1) if cat_tgt else 0
    cat_ct = float(cat_ctds_map.get(nv, 0.0))
    cat_m = float(cat_mtd_map.get(nv, 0.0))
    cat_m_pct = round(cat_m / cat_ct * 100, 1) if cat_ct else 0

    brand_tgt = int(brand_target_map.get(nv, 0))
    brand_act = int(brand_actual_map.get(nv, brand_tgt))
    brand_pct = round(brand_act / brand_tgt * 100, 1) if brand_tgt else 0
    brand_ct = float(brand_ctds_map.get(nv, 0.0))
    brand_m = float(brand_mtd_map.get(nv, 0.0))
    brand_m_pct = round(brand_m / brand_ct * 100, 1) if brand_ct else 0

    rows.append({
        'Tên NV': nv,
        'VIP MCH': v_tgt,
        'Đã Mua (VIP)': v_act,
        '% MTD (VIP)': f'{v_pct}%',
        # KPI sau VIP (điền sau khi có kpi_maps)
        'CT DS': 0, 'TH DS': 0, '% MTD DS': '0%',
        'CT PC_BT': 0, 'TH PC_BT': 0, '% MTD PC_BT': '0%',
        'CT LPPC': 0.0, 'TH LPPC': 0.0, '% MTD LPPC': '0%',
        'CT Xanh': 0, 'TH Xanh': 0, '% MTD Xanh': '0%',
        'CT Vàng': 0, 'TH Vàng': 0, '% MTD Vàng': '0%',
        'CT PC_ON': 0, 'TH PC_ON': 0, '% MTD PC_ON': '0%',
        'KH Combo OFF': off_tgt,
        'Đã Mua (OFF)': off_act,
        '% MTD (OFF)': f'{off_pct}%',
        'KH Combo ON': on_tgt,
        'Đã Mua (ON)': on_act,
        '% MTD (ON)': f'{on_pct}%',
        'MBS Cat': cat_tgt,
        'Đã Mua (Cat)': cat_act,
        '% MTD (Cat)': f'{cat_pct}%',
        'CT DS (Cat)': cat_ct,
        'MTD (Cat)': cat_m,
        '% MTD DS (Cat)': f'{cat_m_pct}%',
        'MBS Brand': brand_tgt,
        'Đã Mua (Brand)': brand_act,
        '% MTD (Brand)': f'{brand_pct}%',
        'CT DS (Brand)': brand_ct,
        'MTD (Brand)': brand_m,
        '% MTD DS (Brand)': f'{brand_m_pct}%',
    })

  df_out = pd.DataFrame(rows)
  if not df_out.empty:
    df_out = df_out.sort_values('Tên NV', ascending=True).reset_index(
        drop=True
    )
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))

    # ---- Gắn KPI (sau VIP MCH) ----
    if targets is None:
      try:
        targets = get_targets()
      except Exception:
        targets = {}
    try:
      _to_tgt = get_turnover_targets()
    except Exception:
      _to_tgt = {}

    def _norm_name(s):
      return ' '.join(str(s).strip().lower().split())

    def _find_ct_col(cols):
      for c in cols:
        cl = str(c).lower()
        if 'chỉ tiêu' in cl or 'chi tieu' in cl:
          return c
      for c in ('Chỉ Tiêu KPI', 'Chỉ Tiêu MCP', 'Chỉ Tiêu Doanh Số', 'Chỉ Tiêu', 'Target'):
        if c in cols:
          return c
      return None

    def _find_mtd_col(cols, prefer=None):
      if prefer:
        for p in prefer:
          if p in cols:
            return p
      for c in cols:
        cl = str(c).lower()
        if cl in ('mtd', 'doanh số mtd', 'doanh so mtd'):
          return c
      return None

    def _apply_kpi_df(df_k, c_ct, c_th, c_pct, as_float=False):
      if df_k is None or df_k.empty:
        return
      name_col = None
      for c in ('Tên NVBH', 'Tên NV', 'SM Name'):
        if c in df_k.columns:
          name_col = c
          break
      if not name_col:
        return
      body = df_k[~df_k[name_col].astype(str).str.upper().str.contains(
          'TOTAL|TỔNG', na=False, regex=True
      )].copy()
      col_ct = _find_ct_col(body.columns)
      col_mtd = _find_mtd_col(
          body.columns,
          prefer=['Doanh Số MTD', 'MTD', 'Thực Hiện'] if 'Doanh Số MTD' in body.columns else ['MTD'],
      )
      col_pct = '% MTD' if '% MTD' in body.columns else None
      if not col_mtd and not col_pct:
        return
      name_to_idx = {
          _norm_name(v): i
          for i, v in df_out['Tên NV'].astype(str).items()
      }
      for _, kr in body.iterrows():
        nm = _norm_name(kr[name_col])
        if nm not in name_to_idx:
          continue
        idx = name_to_idx[nm]
        if col_ct is not None and pd.notna(kr.get(col_ct)):
          try:
            v = float(kr[col_ct])
            df_out.at[idx, c_ct] = round(v, 2) if as_float else int(round(v))
          except Exception:
            pass
        if col_mtd is not None and pd.notna(kr.get(col_mtd)):
          try:
            v = float(kr[col_mtd])
            df_out.at[idx, c_th] = round(v, 2) if as_float else int(round(v))
          except Exception:
            pass
        if col_pct is not None and pd.notna(kr.get(col_pct)):
          df_out.at[idx, c_pct] = str(kr[col_pct])
        elif col_ct is not None and col_mtd is not None:
          try:
            ct = float(kr[col_ct]); th = float(kr[col_mtd])
            df_out.at[idx, c_pct] = f'{round(th / ct * 100, 1)}%' if ct else '0%'
          except Exception:
            pass

    # TURNOVER — hàm riêng
    _mcp_kpi = mcp_filtered if effective_thu_list else mcp_df

    try:
      # CT lấy full tháng (target); TH lấy data đã lọc CH theo Thứ
      df_to_ct, _, _ = build_turnover_report(df, report_date, _to_tgt, filter_nv)
      _apply_kpi_df(df_to_ct, 'CT DS', 'TH DS', '% MTD DS', as_float=False)
      # TH Doanh Số theo Thứ/chu kỳ: tổng DS các ngày khớp weekday
      # → chia cho số ngày khớp đã trôi qua để ra TH/ngày (cùng đơn vị CT ngày)
      if effective_thu_list:
        try:
          _rd = report_date if isinstance(report_date, date) else pd.Timestamp(report_date).date()
        except Exception:
          _rd = report_date
        wdays = _weekdays_from_thu_filter(effective_thu_list)
        # số ngày bán (weekday khớp) từ đầu tháng → report_date
        n_days = 0
        try:
          _cur = date(_rd.year, _rd.month, 1)
          while _cur <= _rd:
            if _cur.weekday() in wdays:
              # trừ CN đã loại vì wdays không có 6=Sun; trừ lễ nếu có
              n_days += 1
            _cur += timedelta(days=1)
        except Exception:
          n_days = 1
        n_days = max(n_days, 1)

        df_to_th, _, _ = build_turnover_report(df_kpi, report_date, _to_tgt, filter_nv)
        if df_to_th is not None and not df_to_th.empty:
          name_col = 'Tên NVBH' if 'Tên NVBH' in df_to_th.columns else None
          mtd_col = 'Doanh Số MTD' if 'Doanh Số MTD' in df_to_th.columns else None
          if name_col and mtd_col:
            body = df_to_th[~df_to_th[name_col].astype(str).str.upper().str.contains(
                'TOTAL|TỔNG', na=False, regex=True
            )]
            name_to_idx = {
                ' '.join(str(v).strip().lower().split()): i
                for i, v in df_out['Tên NV'].astype(str).items()
            }
            for _, kr in body.iterrows():
              nm = ' '.join(str(kr[name_col]).strip().lower().split())
              if nm not in name_to_idx:
                continue
              idx = name_to_idx[nm]
              try:
                th_sum = float(kr[mtd_col])
              except Exception:
                th_sum = 0.0
              th_day = th_sum / n_days
              df_out.at[idx, 'TH DS'] = int(round(th_day))
              try:
                ct = float(df_out.at[idx, 'CT DS'])
                # CT lúc này vẫn là tháng; CT ngày apply sau — tạm % theo tháng CT
                df_out.at[idx, '% MTD DS'] = (
                    f'{round(th_day / ct * 100, 1)}%' if ct else '0%'
                )
              except Exception:
                pass
    except Exception:
      pass

    for rt, c_ct, c_th, c_pct, as_f in [
        ('PC_BT', 'CT PC_BT', 'TH PC_BT', '% MTD PC_BT', False),
        ('ASO_FOCUS', 'CT Xanh', 'TH Xanh', '% MTD Xanh', False),
        ('ASO_FOCUS_2', 'CT Vàng', 'TH Vàng', '% MTD Vàng', False),
        ('PC_ON', 'CT PC_ON', 'TH PC_ON', '% MTD PC_ON', False),
    ]:
      try:
        df_k, _, _ = build_report(
            df_kpi, report_date, targets, rt, filter_nv, mcp_df=_mcp_kpi
        )
        _apply_kpi_df(df_k, c_ct, c_th, c_pct, as_float=as_f)
      except Exception:
        pass

    # ---- LPPC riêng: map chắc chắn CT/TH/% ----
    try:
      df_lppc, _, _ = build_report(
          df_kpi, report_date, targets, 'LPPC', filter_nv, mcp_df=_mcp_kpi
      )
      if df_lppc is not None and not df_lppc.empty:
        name_col = 'Tên NVBH' if 'Tên NVBH' in df_lppc.columns else None
        if name_col:
          body = df_lppc[~df_lppc[name_col].astype(str).str.upper().str.contains(
              'TOTAL|TỔNG', na=False, regex=True
          )].copy()
          col_ct = 'Chỉ Tiêu KPI' if 'Chỉ Tiêu KPI' in body.columns else _find_ct_col(body.columns)
          col_mtd = 'MTD' if 'MTD' in body.columns else None
          col_pct = '% MTD' if '% MTD' in body.columns else None
          # moc mặc định nếu thiếu target
          try:
            _moc = float(get_month_cfg().get('lppc_moc', 4.3) or 4.3)
          except Exception:
            _moc = 4.3
          lookup = {}
          for _, kr in body.iterrows():
            nm = _norm_name(kr[name_col])
            if not nm:
              continue
            try:
              ct = float(kr[col_ct]) if col_ct and pd.notna(kr.get(col_ct)) else _moc
            except Exception:
              ct = _moc
            if not ct:
              ct = _moc
            try:
              th = float(kr[col_mtd]) if col_mtd and pd.notna(kr.get(col_mtd)) else 0.0
            except Exception:
              th = 0.0
            if col_pct and pd.notna(kr.get(col_pct)):
              pct = str(kr[col_pct])
            else:
              pct = f'{round(th / ct * 100, 1)}%' if ct else '0%'
            lookup[nm] = (round(ct, 2), round(th, 2), pct)
          for i, nv in df_out['Tên NV'].astype(str).items():
            key = _norm_name(nv)
            if key in lookup:
              ct, th, pct = lookup[key]
              df_out.at[i, 'CT LPPC'] = ct
              df_out.at[i, 'TH LPPC'] = th
              df_out.at[i, '% MTD LPPC'] = pct
    except Exception:
      pass

    # Khi lọc Thứ/Chu kỳ: CT ngày = CT tháng / số ngày làm việc tháng
    # (Doanh Số, PC BT, ASO Xanh/Vàng, PC ON). LPPC giữ mốc lương.
    # TH = data đã lọc CH theo Thứ. VIP/Combo/MBS đã lọc theo Thứ sẵn.
    if effective_thu_list:
      try:
        _rd = report_date if isinstance(report_date, date) else pd.Timestamp(report_date).date()
        _wd, _, _, _ = get_timegone_stats(_rd)
        _wd = int(_wd or 0)
      except Exception:
        _wd = 0
      if _wd > 0:
        _ct_day_cols = [
            ('CT DS', 'TH DS', '% MTD DS', False),
            ('CT PC_BT', 'TH PC_BT', '% MTD PC_BT', False),
            ('CT Xanh', 'TH Xanh', '% MTD Xanh', False),
            ('CT Vàng', 'TH Vàng', '% MTD Vàng', False),
            ('CT PC_ON', 'TH PC_ON', '% MTD PC_ON', False),
        ]
        for i, row in df_out.iterrows():
          for c_ct, c_th, c_pct, as_f in _ct_day_cols:
            try:
              ct_month = float(row.get(c_ct, 0) or 0)
              th0 = float(row.get(c_th, 0) or 0)
              ct_day = ct_month / _wd
              if as_f:
                df_out.at[i, c_ct] = round(ct_day, 2)
              else:
                df_out.at[i, c_ct] = int(round(ct_day))
              ct_use = float(df_out.at[i, c_ct])
              df_out.at[i, c_pct] = (
                  f'{round(th0 / ct_use * 100, 1)}%' if ct_use else '0%'
              )
            except Exception:
              pass

    tot_v_tgt = int(df_out['VIP MCH'].sum())
    tot_v_act = int(df_out['Đã Mua (VIP)'].sum())
    tot_v_pct = round(tot_v_act / tot_v_tgt * 100, 1) if tot_v_tgt else 0

    tot_off_tgt = int(df_out['KH Combo OFF'].sum())
    tot_off_act = int(df_out['Đã Mua (OFF)'].sum())
    tot_off_pct = (
        round(tot_off_act / tot_off_tgt * 100, 1) if tot_off_tgt else 0
    )

    tot_on_tgt = int(df_out['KH Combo ON'].sum())
    tot_on_act = int(df_out['Đã Mua (ON)'].sum())
    tot_on_pct = round(tot_on_act / tot_on_tgt * 100, 1) if tot_on_tgt else 0

    tot_cat_tgt = int(df_out['MBS Cat'].sum())
    tot_cat_act = int(df_out['Đã Mua (Cat)'].sum())
    tot_cat_pct = round(tot_cat_act / tot_cat_tgt * 100, 1) if tot_cat_tgt else 0
    tot_cat_ct = float(df_out['CT DS (Cat)'].sum())
    tot_cat_m = float(df_out['MTD (Cat)'].sum())
    tot_cat_m_pct = (
        round(tot_cat_m / tot_cat_ct * 100, 1) if tot_cat_ct else 0
    )

    tot_brand_tgt = int(df_out['MBS Brand'].sum())
    tot_brand_act = int(df_out['Đã Mua (Brand)'].sum())
    tot_brand_pct = (
        round(tot_brand_act / tot_brand_tgt * 100, 1) if tot_brand_tgt else 0
    )
    tot_brand_ct = float(df_out['CT DS (Brand)'].sum())
    tot_brand_m = float(df_out['MTD (Brand)'].sum())
    tot_brand_m_pct = (
        round(tot_brand_m / tot_brand_ct * 100, 1) if tot_brand_ct else 0
    )

    def _sum_col(c):
      return float(pd.to_numeric(df_out[c], errors='coerce').fillna(0).sum()) if c in df_out.columns else 0
    def _pct_s(th, ct):
      return f'{round(th / ct * 100, 1)}%' if ct else '0%'

    tot_ds_ct, tot_ds_th = _sum_col('CT DS'), _sum_col('TH DS')
    tot_pcbt_ct, tot_pcbt_th = _sum_col('CT PC_BT'), _sum_col('TH PC_BT')
    # LPPC team = weighted average via total isn't exact; dùng mean non-zero
    _lppc_ct = pd.to_numeric(df_out['CT LPPC'], errors='coerce').fillna(0) if 'CT LPPC' in df_out.columns else pd.Series([0.0])
    _lppc_th = pd.to_numeric(df_out['TH LPPC'], errors='coerce').fillna(0) if 'TH LPPC' in df_out.columns else pd.Series([0.0])
    # CT team = mốc phổ biến (mode/mean của CT > 0); TH team = mean TH
    _ct_pos = _lppc_ct[_lppc_ct > 0]
    tot_lppc_ct = round(float(_ct_pos.mean()), 2) if len(_ct_pos) else 0
    _th_pos = _lppc_th[_lppc_th > 0]
    tot_lppc_th = round(float(_th_pos.mean()), 2) if len(_th_pos) else round(float(_lppc_th.mean()), 2) if len(_lppc_th) else 0
    tot_xanh_ct, tot_xanh_th = _sum_col('CT Xanh'), _sum_col('TH Xanh')
    tot_vang_ct, tot_vang_th = _sum_col('CT Vàng'), _sum_col('TH Vàng')
    tot_pcon_ct, tot_pcon_th = _sum_col('CT PC_ON'), _sum_col('TH PC_ON')

    total_row = pd.DataFrame([{
        'STT': '-',
        'Tên NV': 'TỔNG CỘNG',
        'VIP MCH': tot_v_tgt,
        'Đã Mua (VIP)': tot_v_act,
        '% MTD (VIP)': f'{tot_v_pct}%',
        'CT DS': int(tot_ds_ct), 'TH DS': int(tot_ds_th), '% MTD DS': _pct_s(tot_ds_th, tot_ds_ct),
        'CT PC_BT': int(tot_pcbt_ct), 'TH PC_BT': int(tot_pcbt_th), '% MTD PC_BT': _pct_s(tot_pcbt_th, tot_pcbt_ct),
        'CT LPPC': tot_lppc_ct, 'TH LPPC': tot_lppc_th, '% MTD LPPC': _pct_s(tot_lppc_th, tot_lppc_ct) if tot_lppc_ct else '0%',
        'CT Xanh': int(tot_xanh_ct), 'TH Xanh': int(tot_xanh_th), '% MTD Xanh': _pct_s(tot_xanh_th, tot_xanh_ct),
        'CT Vàng': int(tot_vang_ct), 'TH Vàng': int(tot_vang_th), '% MTD Vàng': _pct_s(tot_vang_th, tot_vang_ct),
        'CT PC_ON': int(tot_pcon_ct), 'TH PC_ON': int(tot_pcon_th), '% MTD PC_ON': _pct_s(tot_pcon_th, tot_pcon_ct),
        'KH Combo OFF': tot_off_tgt,
        'Đã Mua (OFF)': tot_off_act,
        '% MTD (OFF)': f'{tot_off_pct}%',
        'KH Combo ON': tot_on_tgt,
        'Đã Mua (ON)': tot_on_act,
        '% MTD (ON)': f'{tot_on_pct}%',
        'MBS Cat': tot_cat_tgt,
        'Đã Mua (Cat)': tot_cat_act,
        '% MTD (Cat)': f'{tot_cat_pct}%',
        'CT DS (Cat)': tot_cat_ct,
        'MTD (Cat)': tot_cat_m,
        '% MTD DS (Cat)': f'{tot_cat_m_pct}%',
        'MBS Brand': tot_brand_tgt,
        'Đã Mua (Brand)': tot_brand_act,
        '% MTD (Brand)': f'{tot_brand_pct}%',
        'CT DS (Brand)': tot_brand_ct,
        'MTD (Brand)': tot_brand_m,
        '% MTD DS (Brand)': f'{tot_brand_m_pct}%',
    }])
    df_out = pd.concat([df_out, total_row], ignore_index=True)

  return df_out


def render_summary_html_table(df, selected_metrics):
  """Bảng Tổng Hợp — format sticky STT + Tên NV giống Báo Cáo Trưng Bày."""
  if df is None or df.empty:
    return '<p>Không có dữ liệu báo cáo tổng hợp.</p>'
  df = df.drop(columns=['Mã NVBH'], errors='ignore')

  has_vip = 'VIP MCH' in selected_metrics
  has_ds = 'Doanh Số' in selected_metrics
  has_pcbt = 'PC BT' in selected_metrics
  has_lppc = 'LPPC' in selected_metrics
  has_xanh = 'ASO Trận Xanh' in selected_metrics
  has_vang = 'ASO Trận Vàng' in selected_metrics
  has_pcon = 'PC Kênh ON' in selected_metrics
  has_off = 'KH Combo OFF' in selected_metrics
  has_on = 'KH Combo ON' in selected_metrics
  has_cat = 'MBS Cat' in selected_metrics
  has_brand = 'MBS Brand' in selected_metrics

  max_name = 12
  if 'Tên NV' in df.columns:
    for n in df['Tên NV'].astype(str):
      max_name = max(max_name, len(n))
  name_w = max(140, min(280, max_name * 9 + 24))

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 5px;font-size:11px;'
      'white-space:nowrap;'
  )
  td = 'border:1px solid #bce2f5 !important;padding:5px 4px;font-size:12px;white-space:nowrap;'
  tot_style = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;border:1px solid #2b6cb0 !important;'
      'padding:5px 4px;font-size:12px;'
  )
  sticky_stt_h = f'{th}position:sticky;left:0;z-index:6;min-width:44px;max-width:44px;'
  sticky_ten_h = f'{th}position:sticky;left:44px;z-index:6;min-width:{name_w}px;'
  sticky_stt_c = f'{td}position:sticky;left:0;z-index:4;min-width:44px;max-width:44px;text-align:center;'
  sticky_ten_c = f'{td}position:sticky;left:44px;z-index:4;min-width:{name_w}px;text-align:left;font-weight:600;'
  sticky_stt_t = f'{tot_style}position:sticky;left:0;z-index:5;min-width:44px;text-align:center;'
  sticky_ten_t = f'{tot_style}position:sticky;left:44px;z-index:5;min-width:{name_w}px;text-align:left;'

  groups = []
  if has_vip:
    groups.append(('VIP MCH', [
        ('VIP MCH', 'VIP MCH', False, False),
        ('Đã Mua (VIP)', 'Đã Mua', False, False),
        ('% MTD (VIP)', '% MTD', True, False),
    ]))
  if has_ds:
    groups.append(('Doanh Số', [
        ('CT DS', 'CT', False, True),
        ('TH DS', 'TH', False, True),
        ('% MTD DS', '% MTD', True, False),
    ]))
  if has_pcbt:
    groups.append(('PC BT', [
        ('CT PC_BT', 'CT', False, False),
        ('TH PC_BT', 'TH', False, False),
        ('% MTD PC_BT', '% MTD', True, False),
    ]))
  if has_lppc:
    groups.append(('LPPC', [
        ('CT LPPC', 'CT', False, False),
        ('TH LPPC', 'TH', False, False),
        ('% MTD LPPC', '% MTD', True, False),
    ]))
  if has_xanh:
    groups.append(('ASO Trận Xanh', [
        ('CT Xanh', 'CT', False, False),
        ('TH Xanh', 'TH', False, False),
        ('% MTD Xanh', '% MTD', True, False),
    ]))
  if has_vang:
    groups.append(('ASO Trận Vàng', [
        ('CT Vàng', 'CT', False, False),
        ('TH Vàng', 'TH', False, False),
        ('% MTD Vàng', '% MTD', True, False),
    ]))
  if has_pcon:
    groups.append(('PC Kênh ON', [
        ('CT PC_ON', 'CT', False, False),
        ('TH PC_ON', 'TH', False, False),
        ('% MTD PC_ON', '% MTD', True, False),
    ]))
  if has_off:
    groups.append(('KH Combo OFF', [
        ('KH Combo OFF', 'KH Combo OFF', False, False),
        ('Đã Mua (OFF)', 'Đã Mua', False, False),
        ('% MTD (OFF)', '% MTD', True, False),
    ]))
  if has_on:
    groups.append(('KH Combo ON', [
        ('KH Combo ON', 'KH Combo ON', False, False),
        ('Đã Mua (ON)', 'Đã Mua', False, False),
        ('% MTD (ON)', '% MTD', True, False),
    ]))
  if has_cat:
    groups.append(('MBS Cat (K VNĐ)', [
        ('MBS Cat', 'MBS Cat', False, False),
        ('Đã Mua (Cat)', 'Đã Mua', False, False),
        ('% MTD (Cat)', '% MTD', True, False),
        ('CT DS (Cat)', 'CT DS', False, True),
        ('MTD (Cat)', 'MTD', False, True),
        ('% MTD DS (Cat)', '% MTD', True, False),
    ]))
  if has_brand:
    groups.append(('MBS Brand (K VNĐ)', [
        ('MBS Brand', 'MBS Brand', False, False),
        ('Đã Mua (Brand)', 'Đã Mua', False, False),
        ('% MTD (Brand)', '% MTD', True, False),
        ('CT DS (Brand)', 'CT DS', False, True),
        ('MTD (Brand)', 'MTD', False, True),
        ('% MTD DS (Brand)', '% MTD', True, False),
    ]))

  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:12px;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;width:max-content;min-width:100%;">',
      '<thead>',
      '<tr>',
      f'<th rowspan="2" style="{sticky_stt_h}">STT</th>',
      f'<th rowspan="2" style="{sticky_ten_h}">Tên NV</th>',
  ]
  for title, cols in groups:
    html.append(f'<th colspan="{len(cols)}" style="{th}">{title}</th>')
  html.append('</tr><tr>')
  for _, cols in groups:
    for _, sub, _, _ in cols:
      html.append(f'<th style="{th}">{sub}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = (
        str(row.get('Tên NV', '')).strip() == 'TỔNG CỘNG'
        or 'TOTAL' in str(row.get('Tên NV', '')).upper()
        or 'TỔNG' in str(row.get('Tên NV', '')).upper()
    )
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr' + (' class="row-total"' if is_tot else '') + '>')
    stt = row.get('STT', '')
    ten = row.get('Tên NV', '')
    if is_tot:
      html.append(f'<td class="row-total-cell" style="{sticky_stt_t}">{stt}</td>')
      html.append(f'<td class="row-total-cell" style="{sticky_ten_t}">{ten}</td>')
    else:
      html.append(f'<td style="{sticky_stt_c}background-color:{bg} !important;">{stt}</td>')
      html.append(f'<td style="{sticky_ten_c}background-color:{bg} !important;">{ten}</td>')

    for _, cols in groups:
      for col, _, is_pct, is_money in cols:
        val = row.get(col, '')
        if pd.isna(val):
          val = ''
        if is_money and val != '':
          try:
            val = format_scaled_thousand(val)
          except Exception:
            try:
              val = format_number_vn(val)
            except Exception:
              pass
        if is_tot:
          if is_pct:
            cls = color_pct_class(val)
            style_bg = color_pct_bg(val)
            html.append(
                f'<td align="center" data-colored="1" class="{cls} row-total-cell" '
                f'style="{style_bg}font-weight:900 !important;text-align:center !important;">{val}</td>'
            )
          else:
            align = 'right' if is_money else 'center'
            html.append(
                f'<td class="row-total-cell" style="{tot_style}text-align:{align} !important;">{val}</td>'
            )
        else:
          if is_pct:
            cls = color_pct_class(val)
            style_bg = color_pct_bg(val)
            html.append(
                f'<td align="center" data-colored="1" class="{cls}" '
                f'style="{td}{style_bg}text-align:center !important;">{val}</td>'
            )
          else:
            align = 'right' if is_money else 'center'
            html.append(
                f'<td style="{td}background-color:{bg} !important;text-align:{align};">{val}</td>'
            )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def render_html_table(df, freeze_cols=None):
  """Bảng KPI format Trưng Bày: sticky cột đầu + cuộn ngang.
  freeze_cols: list cột cố định (mặc định STT + Tên NVBH;
               MBS Cat/Brand: STT, Tên nhóm, Outlet Code, Tên CH).
  """
  df = df.drop(columns=['Mã NVBH'], errors='ignore').copy()
  cols = list(df.columns)

  # Auto detect freeze columns cho MBS detail
  if freeze_cols is None:
    mbs_keys = ['Tên nhóm', 'Outlet Code', 'Tên CH']
    if all(c in cols for c in mbs_keys):
      freeze_cols = [c for c in ['STT', 'Tên nhóm', 'Outlet Code', 'Tên CH'] if c in cols]
    else:
      freeze_cols = [c for c in ['STT', 'Tên NVBH', 'Tên NV'] if c in cols]

  # unique preserve order
  seen = set()
  freeze_cols = [c for c in freeze_cols if c in cols and not (c in seen or seen.add(c))]

  def _col_width(c):
    cl = str(c).lower()
    if c == 'STT':
      return 48
    if 'nhóm' in cl or 'nhom' in cl:
      return 200
    if 'outlet' in cl or 'mã' in cl or 'ma kh' in cl:
      return 100
    if c in ('Tên CH', 'Tên KH') or 'tên ch' in cl:
      return 150
    if 'nvbh' in cl or 'tên nv' in cl:
      max_name = 12
      for n in df[c].astype(str):
        max_name = max(max_name, len(n))
      return max(150, min(260, max_name * 9 + 24))
    return 120

  widths = {}
  left = 0
  for c in freeze_cols:
    w = _col_width(c)
    widths[c] = (left, w)
    left += w

  sh = 'box-shadow:3px 0 5px -2px rgba(0,0,0,.22);'
  th_base = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 8px;font-size:11px;'
      'white-space:nowrap;'
  )

  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:8px;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;'
      'width:max-content;min-width:100%;">',
      '<thead><tr>',
  ]
  for col in cols:
    if col in widths:
      L, w = widths[col]
      html.append(
          f'<th style="{th_base}position:sticky;left:{L}px;z-index:8;'
          f'min-width:{w}px;max-width:{w}px;{sh}">{col}</th>'
      )
    else:
      html.append(f'<th style="{th_base}">{col}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    is_total = (
        'TOTAL' in str(row.get('Tên NVBH', '')).upper()
        or 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
        or 'TOTAL' in str(row.get('Tên NV', '')).upper()
        or 'TỔNG' in str(row.get('Tên NV', '')).upper()
        or 'TOTAL' in str(row.get('Tên nhóm', '')).upper()
        or 'TỔNG' in str(row.get('Tên nhóm', '')).upper()
    )
    if is_total:
      row_bg, row_fg = '#1a365d', '#ffffff'
    else:
      row_bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
      row_fg = '#1a202c'

    html.append('<tr>')
    for col in cols:
      val = row[col]
      if pd.isna(val):
        val = ''
      elif isinstance(val, (float, np.floating)):
        if float(val).is_integer():
          val = int(val)
        else:
          val = round(float(val), 2)

      is_sticky = col in widths
      if is_sticky:
        L, w = widths[col]
        sticky = (
            f'position:sticky;left:{L}px;z-index:{"7" if is_total else "5"};'
            f'min-width:{w}px;max-width:{w}px;'
            f'background-color:{row_bg} !important;color:{row_fg} !important;{sh}'
        )
      else:
        sticky = f'background-color:{row_bg} !important;color:{row_fg} !important;'

      is_pct_col = (
          col in [
              '% MTD', '% MTD (OFF)', '% MTD (ON)', '% MTD OFF', '% MTD ON',
              '% Hoàn Thành', '% TH', '% PC/VT OFF', '% PC/Plan ON', '% TH SO',
              '% TH Xanh', '% TH Vàng', '% Active',
          ]
          or (isinstance(col, str) and col.strip().startswith('%'))
      )

      salary_cls, salary_style = salary_metric_style(_CURRENT_SALARY_KPI, col, val)
      if (salary_cls or salary_style) and not is_sticky:
        align_salary = 'center' if ('%' in str(col) or col in ['MTD', 'Thực Hiện Ngày']) else 'right'
        html.append(
            f'<td align="{align_salary}" data-colored="1" class="{salary_cls}" '
            f'style="{salary_style}{sticky} text-align:{align_salary} !important;'
            f'white-space:nowrap;">{val}</td>'
        )
      elif is_pct_col and not is_sticky:
        style_bg = color_pct_bg(val)
        cls = color_pct_class(val)
        html.append(
            f'<td align="center" data-colored="1" class="{cls}" '
            f'style="{style_bg} text-align:center !important;font-weight:700 !important;'
            f'white-space:nowrap;">{val}</td>'
        )
      elif is_total and not is_sticky:
        align = 'center' if ('%' in str(col) or col == 'STT') else 'right'
        if is_pct_col or (isinstance(val, str) and '%' in str(val)):
          style_bg = color_pct_bg(val)
          cls = color_pct_class(val)
          html.append(
              f'<td align="center" data-colored="1" class="{cls}" '
              f'style="{style_bg} font-weight:900 !important;'
              f'text-align:center !important;white-space:nowrap;">{val}</td>'
          )
        else:
          html.append(
              f'<td data-colored="1" class="row-total-cell" '
              f'style="background-color:#1a365d !important;color:#ffffff !important;'
              f'font-weight:900 !important;text-align:{align} !important;'
              f'white-space:nowrap;border-color:#2b6cb0 !important;">{val}</td>'
          )
      elif is_sticky:
        align = 'center' if col == 'STT' else 'left'
        fw = '900' if is_total else '600'
        html.append(
            f'<td style="{sticky}text-align:{align} !important;font-weight:{fw} !important;'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'
            f'border:1px solid {"#2b6cb0" if is_total else "#bce2f5"} !important;">{val}</td>'
        )
      else:
        align = (
            'center'
            if col in [
                'STT', 'Lịch Viếng Thăm Hôm Nay',
                'Nhóm KH VIP3', 'Nhóm KH VIP5', 'Nhóm KH VIPSI',
                'Nhóm KH CH Lẻ', 'Nhóm KH Kênh ON',
                'Thực Hiện Ngày', 'MTD',
                'Phát sinh Ngày (OFF)', 'MTD (OFF)',
                'Phát sinh Ngày (ON)', 'MTD (ON)',
                'Chỉ Tiêu KPI', 'Target (OFF)', 'Target (ON)',
                'Thứ VT', 'Member type', 'Đạt nhiệm vụ',
            ]
            else 'right'
        )
        if col in ['Chỉ Tiêu Doanh Số', 'Doanh Số MTD', 'Thực Hiện Ngày', 'Actual', 'Target']:
          align = 'right'
        if col in ['Tên NVBH', 'Tên NV', 'Tên CH', 'Tên KH']:
          align = 'left'
        html.append(
            f'<td style="{sticky}text-align:{align};white-space:nowrap;">{val}</td>'
        )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



# ====================== BÁO CÁO MBS CAT (6 NHÓM) ======================

def check_mbs_mission(df_outlet, member_type, col_loai='_loai', col_actual='_actual'):
  """Kiểm tra đạt nhiệm vụ theo Member type (CAT1/2/3 hoặc BRAND1/2/3).

  LUÔN dùng Doanh số thực đạt (Actual) — KHÔNG dùng Not Cancel/Pending.

  CAT1 / BRAND1: >= 1 NEW có DS >= 200.000
  CAT2 / BRAND2: Duy trì đủ FOCUS, mỗi FOCUS >= 200.000 (KHÔNG bắt buộc NEW)
  CAT3 / BRAND3: Duy trì đủ FOCUS (>=200k mỗi cái) VÀ >= 1 NEW >= 200.000
  """
  mt = str(member_type or '').strip().upper().replace(' ', '')
  loai = df_outlet[col_loai].astype(str).str.upper()
  # Bắt buộc cột Actual (không phải Not Cancel/Pending)
  if col_actual not in df_outlet.columns and '_actual' in df_outlet.columns:
    col_actual = '_actual'
  act = pd.to_numeric(df_outlet[col_actual], errors='coerce').fillna(0)

  has_new = bool(((loai.str.contains('NEW', na=False)) & (act >= 200000)).any())

  focus_mask = loai.str.contains('FOCUS', na=False)
  if focus_mask.any():
    # Mỗi dòng FOCUS phải >= 200.000
    all_focus_ok = bool((act[focus_mask] >= 200000).all())
  else:
    # Không có FOCUS nào trong data -> coi như không cần duy trì FOCUS
    all_focus_ok = True

  if mt in ('CAT1', 'BRAND1'):
    return has_new
  if mt in ('CAT2', 'BRAND2'):
    return all_focus_ok  # không bắt buộc NEW
  if mt in ('CAT3', 'BRAND3'):
    return all_focus_ok and has_new
  # fallback: giữ logic cũ
  return has_new



def render_mbs_pie_chart(df_show, title='Tỷ lệ KH theo Nhóm'):
  """Biểu đồ tròn tỷ lệ từng nhóm / tổng KH đang hiển thị."""
  try:
    import plotly.graph_objects as go
    if df_show is None or df_show.empty or 'Nhóm' not in df_show.columns:
      return
    cnt = df_show.groupby('Nhóm').size()
    if 'Tên nhóm' in df_show.columns:
      name_map = (
          df_show.groupby('Nhóm')['Tên nhóm'].first().astype(str).to_dict()
      )
    else:
      name_map = {g: f'Nhóm {g}' for g in cnt.index}
    labels = [name_map.get(g, f'Nhóm {g}') for g in cnt.index]
    values = cnt.tolist()
    total = sum(values)
    # Palette tương phản rõ (không lặp màu)
    colors = {
        1: '#38a169',  # xanh lá đậm
        2: '#dd6b20',  # cam
        3: '#3182ce',  # xanh dương
        4: '#d69e2e',  # vàng/amber
        5: '#e53e3e',  # đỏ
        6: '#805ad5',  # tím
    }
    fallback = ['#2b6cb0', '#c05621', '#276749', '#b7791f', '#c53030', '#6b46c1']
    marker_colors = []
    for i, g in enumerate(cnt.index):
      try:
        marker_colors.append(colors.get(int(g), fallback[i % len(fallback)]))
      except Exception:
        marker_colors.append(fallback[i % len(fallback)])
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.35,
        marker=dict(colors=marker_colors, line=dict(color='#fff', width=1)),
        textinfo='percent+label',
        textposition='outside',
        hovertemplate='%{label}<br>%{value} KH (%{percent})<extra></extra>',
    )])
    fig.update_layout(
        title=dict(
            text=f'{title} (Tổng {total:,} KH)'.replace(',', '.'),
            font=dict(size=14, color='#1a365d'),
            x=0.5, xanchor='center',
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        height=380,
        showlegend=True,
        legend=dict(orientation='h', y=-0.05, x=0.5, xanchor='center', font=dict(size=11)),
        paper_bgcolor='white',
    )
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True, 'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    })
  except Exception as e:
    st.caption(f'Không vẽ được chart nhóm: {e}')


def build_mbs_cat_report(df_cat, filter_nv=None, mcp_df=None):
  """Phân loại KH MBS CAT thành 6 nhóm.
  Target = Doanh số nền tảng của OUTLET
  Actual = Tổng Doanh số thực đạt của CAT (sau CK)
  Nhiệm vụ = có >= 1 Cat NEW với DS >= 200.000
  Thứ VT lấy từ Data_MCP (cột Thứ) theo Outlet Code
  """
  empty = {'groups': {}, 'df_detail': pd.DataFrame(), 'total_kh': 0}
  if df_cat is None or df_cat.empty:
    return empty

  df = df_cat.copy()
  c_nv = find_col(df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
  c_ma = find_col(df, ['Outlet Code', 'Outlet_code', 'Mã CH'])
  c_ten = find_col(df, ['Outlet Name', 'Outlet_name', 'Tên CH'])
  c_member = find_col(df, ['Member type', 'Member Type', 'Phân loại CAT'])
  c_loai = find_col(df, ['Phân loại cat', 'Phan loai cat', 'Loại cat'])
  c_target = find_col(
      df,
      [
          'Doanh số nền tảng của OUTLET',
          'Doanh so nen tang',
          'Target',
          'Chỉ tiêu',
      ],
  )
  # Actual = Doanh số thực đạt (KHÔNG lấy Not Cancel/Pending)
  c_actual = None
  for c in df.columns:
    cl = str(c).strip().lower()
    if 'not cancel' in cl or 'pending' in cl:
      continue
    if cl == 'doanh số thực đạt của cat' or (
        'thực đạt' in cl and 'cat' in cl
    ):
      c_actual = c
      break
  if not c_actual:
    for c in df.columns:
      cl = str(c).strip().lower()
      if 'not cancel' in cl or 'pending' in cl:
        continue
      if 'thực đạt' in cl or 'doanh so thuc dat' in cl:
        c_actual = c
        break

  # Actual Not Cancel/Pending
  c_actual_nc = None
  for c in df.columns:
    cl = str(c).lower()
    if 'not cancel' in cl or ('pending' in cl and 'thực đạt' in cl):
      c_actual_nc = c
      break
  if not c_actual_nc:
    c_actual_nc = find_col(
        df,
        [
            'Doanh số thực đạt của CAT(Not Cancel/Pending)',
            'Doanh số thực đạt của CAT (Not Cancel/Pending)',
        ],
    )

  if not c_ma or not c_target or not c_actual:
    return empty

  if nv_selected(filter_nv) and c_nv:
    df = filter_df_by_nv(df, c_nv, filter_nv)

  df['_ma'] = df[c_ma].astype(str).str.strip()
  df['_actual'] = pd.to_numeric(df[c_actual], errors='coerce').fillna(0)
  if c_actual_nc and c_actual_nc in df.columns:
    df['_actual_nc'] = pd.to_numeric(
        df[c_actual_nc], errors='coerce'
    ).fillna(0)
  else:
    df['_actual_nc'] = df['_actual']
  df['_target'] = pd.to_numeric(df[c_target], errors='coerce').fillna(0)
  df['_loai'] = (
      df[c_loai].astype(str).str.strip().str.upper() if c_loai else ''
  )

  # Map Thứ VT từ MCP
  thu_map = {}
  if mcp_df is not None and not mcp_df.empty:
    c_ma_mcp = find_col(mcp_df, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    c_thu_mcp = find_col(mcp_df, ['Thứ', 'Frequency', 'Tần suất'])
    if c_ma_mcp and c_thu_mcp:
      tmp = mcp_df[[c_ma_mcp, c_thu_mcp]].copy()
      tmp['_ma'] = tmp[c_ma_mcp].astype(str).str.strip()
      tmp['_thu'] = tmp[c_thu_mcp].astype(str).str.strip()
      thu_map = (
          tmp.drop_duplicates('_ma').set_index('_ma')['_thu'].to_dict()
      )

  actual_by_outlet = df.groupby('_ma')['_actual'].sum()
  actual_nc_by_outlet = df.groupby('_ma')['_actual_nc'].sum()
  target_by_outlet = df.groupby('_ma')['_target'].first()
  nv_by_outlet = (
      df.groupby('_ma')[c_nv].first() if c_nv else pd.Series(dtype=str)
  )
  ten_by_outlet = (
      df.groupby('_ma')[c_ten].first() if c_ten else pd.Series(dtype=str)
  )
  member_by_outlet = (
      df.groupby('_ma')[c_member].first() if c_member else pd.Series(dtype=str)
  )

  rows = []
  for ma in actual_by_outlet.index:
    actual = float(actual_by_outlet.get(ma, 0) or 0)
    actual_nc = float(actual_nc_by_outlet.get(ma, 0) or 0)
    target = float(target_by_outlet.get(ma, 0) or 0)
    # % TH + phân nhóm + nhiệm vụ: chỉ trên Actual (không dùng Not Cancel)
    pct = (actual / target * 100) if target > 0 else (100.0 if actual > 0 else 0.0)
    member = member_by_outlet.get(ma, '') if len(member_by_outlet) else ''
    df_out = df[df['_ma'] == ma]
    has_mission = check_mbs_mission(df_out, member, col_actual='_actual')

    if actual <= 0:
      nhom, nhom_name = 5, 'Nhóm 5 · Chưa phát sinh DS'
    elif actual >= target and has_mission:
      nhom, nhom_name = 1, 'Nhóm 1 · Đã đạt MBS'
    elif actual >= target and not has_mission:
      nhom, nhom_name = 2, 'Nhóm 2 · Đạt DS, thiếu nhiệm vụ'
    elif pct >= 50 and actual < target and has_mission:
      nhom, nhom_name = 3, 'Nhóm 3 · Đạt nhiệm vụ, DS ≥50% Target'
    elif pct >= 60 and actual < target and not has_mission:
      nhom, nhom_name = 4, 'Nhóm 4 · DS ≥60% Target, thiếu nhiệm vụ'
    else:
      nhom, nhom_name = 6, 'Nhóm 6 · Còn lại'

    rows.append({
        'Outlet Code': ma,
        'Tên CH': ten_by_outlet.get(ma, '') if len(ten_by_outlet) else '',
        'Tên NVBH': nv_by_outlet.get(ma, '') if len(nv_by_outlet) else '',
        'Member type': member,
        'Thứ VT': thu_map.get(ma, ''),
        'Actual': actual,
        'Actual (Not Cancel/Pending)': actual_nc,
        'Target': target,
        '% TH': round(pct, 1),
        'Đạt nhiệm vụ': 'Có' if has_mission else 'Không',
        'Nhóm': nhom,
        'Tên nhóm': nhom_name,
    })

  df_detail = pd.DataFrame(rows)
  total_kh = len(df_detail)

  group_meta = {
      1: ('Nhóm 1 · Đã đạt MBS', '#c6f6d5', '#22543d'),
      2: ('Nhóm 2 · Đạt DS, thiếu nhiệm vụ', '#edf2f7', '#2d3748'),
      3: ('Nhóm 3 · Đạt nhiệm vụ, DS ≥50% Target', '#edf2f7', '#2d3748'),
      4: ('Nhóm 4 · DS ≥60% Target, thiếu nhiệm vụ', '#e6fffa', '#234e52'),
      5: ('Nhóm 5 · Chưa phát sinh DS', '#fff5f5', '#c53030'),
      6: ('Nhóm 6 · Còn lại', '#ebf8ff', '#2b6cb0'),
  }

  groups = {}
  for g in range(1, 7):
    sub = (
        df_detail[df_detail['Nhóm'] == g]
        if not df_detail.empty
        else pd.DataFrame()
    )
    kh = len(sub)
    act = float(sub['Actual'].sum()) if kh else 0.0
    tgt = float(sub['Target'].sum()) if kh else 0.0
    pct_th = round(act / tgt * 100, 1) if tgt > 0 else 0.0
    pct_kh = round(kh / total_kh * 100, 1) if total_kh else 0.0
    name, bg, color = group_meta[g]
    groups[g] = {
        'name': name,
        'kh': kh,
        'total_kh': total_kh,
        'pct_kh': pct_kh,
        'actual': act,
        'target': tgt,
        'pct_th': pct_th,
        'bg': bg,
        'color': color,
    }

  return {'groups': groups, 'df_detail': df_detail, 'total_kh': total_kh}


def format_trieu(v):
  """Format số tiền thành triệu VNĐ kiểu 1.300,3"""
  try:
    tr = float(v) / 1_000_000
    s = f'{tr:,.1f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')
  except Exception:
    return '0,0'




def build_mbs_brand_report(df_brand, filter_nv=None, mcp_df=None):
  """Phân loại KH MBS BRAND thành 6 nhóm (logic giống MBS CAT).
  Target = Doanh số nền tảng của OUTLET
  Actual = Tổng Doanh số thực đạt của brand (sau CK)
  Nhiệm vụ = có >= 1 Brand NEW với DS >= 200.000
  """
  empty = {'groups': {}, 'df_detail': pd.DataFrame(), 'total_kh': 0}
  if df_brand is None or df_brand.empty:
    return empty

  df = df_brand.copy()
  c_nv = find_col(df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
  c_ma = find_col(df, ['Outlet Code', 'Outlet_code', 'Mã CH'])
  c_ten = find_col(df, ['Outlet Name', 'Outlet_name', 'Tên CH'])
  c_member = find_col(df, ['Member type', 'Member Type', 'Phân loại CAT'])
  c_loai = find_col(
      df, ['Phân loại brand', 'Phan loai brand', 'Phân loại cat', 'Loại brand']
  )
  c_target = find_col(
      df,
      [
          'Doanh số nền tảng của OUTLET',
          'Doanh so nen tang',
          'Target',
          'Chỉ tiêu',
      ],
  )
  # Actual = Doanh số thực đạt brand (KHÔNG lấy Not Cancel/Pending)
  c_actual = None
  for c in df.columns:
    cl = str(c).strip().lower()
    if 'not cancel' in cl or 'pending' in cl:
      continue
    if cl == 'doanh số thực đạt của brand' or (
        'thực đạt' in cl and 'brand' in cl
    ):
      c_actual = c
      break
  if not c_actual:
    for c in df.columns:
      cl = str(c).strip().lower()
      if 'not cancel' in cl or 'pending' in cl:
        continue
      if 'thực đạt' in cl or 'doanh so thuc dat' in cl:
        c_actual = c
        break

  c_actual_nc = None
  for c in df.columns:
    cl = str(c).lower()
    if ('not cancel' in cl or 'pending' in cl) and (
        'thực đạt' in cl or 'brand' in cl
    ):
      c_actual_nc = c
      break
  if not c_actual_nc:
    c_actual_nc = find_col(
        df,
        [
            'Doanh số thực đạt của brand (Not Cancel/Pending)',
            'Doanh số thực đạt của brand(Not Cancel/Pending)',
        ],
    )

  if not c_ma or not c_target or not c_actual:
    return empty

  if nv_selected(filter_nv) and c_nv:
    df = filter_df_by_nv(df, c_nv, filter_nv)

  df['_ma'] = df[c_ma].astype(str).str.strip()
  df['_actual'] = pd.to_numeric(df[c_actual], errors='coerce').fillna(0)
  if c_actual_nc and c_actual_nc in df.columns:
    df['_actual_nc'] = pd.to_numeric(
        df[c_actual_nc], errors='coerce'
    ).fillna(0)
  else:
    df['_actual_nc'] = df['_actual']
  df['_target'] = pd.to_numeric(df[c_target], errors='coerce').fillna(0)
  df['_loai'] = (
      df[c_loai].astype(str).str.strip().str.upper() if c_loai else ''
  )

  thu_map = {}
  if mcp_df is not None and not mcp_df.empty:
    c_ma_mcp = find_col(mcp_df, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    c_thu_mcp = find_col(mcp_df, ['Thứ', 'Frequency', 'Tần suất'])
    if c_ma_mcp and c_thu_mcp:
      tmp = mcp_df[[c_ma_mcp, c_thu_mcp]].copy()
      tmp['_ma'] = tmp[c_ma_mcp].astype(str).str.strip()
      tmp['_thu'] = tmp[c_thu_mcp].astype(str).str.strip()
      thu_map = (
          tmp.drop_duplicates('_ma').set_index('_ma')['_thu'].to_dict()
      )

  actual_by_outlet = df.groupby('_ma')['_actual'].sum()
  actual_nc_by_outlet = df.groupby('_ma')['_actual_nc'].sum()
  target_by_outlet = df.groupby('_ma')['_target'].first()
  nv_by_outlet = (
      df.groupby('_ma')[c_nv].first() if c_nv else pd.Series(dtype=str)
  )
  ten_by_outlet = (
      df.groupby('_ma')[c_ten].first() if c_ten else pd.Series(dtype=str)
  )
  member_by_outlet = (
      df.groupby('_ma')[c_member].first() if c_member else pd.Series(dtype=str)
  )

  rows = []
  for ma in actual_by_outlet.index:
    actual = float(actual_by_outlet.get(ma, 0) or 0)
    actual_nc = float(actual_nc_by_outlet.get(ma, 0) or 0)
    target = float(target_by_outlet.get(ma, 0) or 0)
    # % TH + phân nhóm + nhiệm vụ: chỉ trên Actual (không dùng Not Cancel)
    pct = (actual / target * 100) if target > 0 else (100.0 if actual > 0 else 0.0)
    member = member_by_outlet.get(ma, '') if len(member_by_outlet) else ''
    df_out = df[df['_ma'] == ma]
    has_mission = check_mbs_mission(df_out, member, col_actual='_actual')

    if actual <= 0:
      nhom, nhom_name = 5, 'Nhóm 5 · Chưa phát sinh DS'
    elif actual >= target and has_mission:
      nhom, nhom_name = 1, 'Nhóm 1 · Đã đạt MBS'
    elif actual >= target and not has_mission:
      nhom, nhom_name = 2, 'Nhóm 2 · Đạt DS, thiếu nhiệm vụ'
    elif pct >= 50 and actual < target and has_mission:
      nhom, nhom_name = 3, 'Nhóm 3 · Đạt nhiệm vụ, DS ≥50% Target'
    elif pct >= 60 and actual < target and not has_mission:
      nhom, nhom_name = 4, 'Nhóm 4 · DS ≥60% Target, thiếu nhiệm vụ'
    else:
      nhom, nhom_name = 6, 'Nhóm 6 · Còn lại'

    rows.append({
        'Outlet Code': ma,
        'Tên CH': ten_by_outlet.get(ma, '') if len(ten_by_outlet) else '',
        'Tên NVBH': nv_by_outlet.get(ma, '') if len(nv_by_outlet) else '',
        'Member type': member,
        'Thứ VT': thu_map.get(ma, ''),
        'Actual': actual,
        'Actual (Not Cancel/Pending)': actual_nc,
        'Target': target,
        '% TH': round(pct, 1),
        'Đạt nhiệm vụ': 'Có' if has_mission else 'Không',
        'Nhóm': nhom,
        'Tên nhóm': nhom_name,
    })

  df_detail = pd.DataFrame(rows)
  total_kh = len(df_detail)

  group_meta = {
      1: ('Nhóm 1 · Đã đạt MBS', '#c6f6d5', '#22543d'),
      2: ('Nhóm 2 · Đạt DS, thiếu nhiệm vụ', '#edf2f7', '#2d3748'),
      3: ('Nhóm 3 · Đạt nhiệm vụ, DS ≥50% Target', '#edf2f7', '#2d3748'),
      4: ('Nhóm 4 · DS ≥60% Target, thiếu nhiệm vụ', '#e6fffa', '#234e52'),
      5: ('Nhóm 5 · Chưa phát sinh DS', '#fff5f5', '#c53030'),
      6: ('Nhóm 6 · Còn lại', '#ebf8ff', '#2b6cb0'),
  }

  groups = {}
  for g in range(1, 7):
    sub = (
        df_detail[df_detail['Nhóm'] == g]
        if not df_detail.empty
        else pd.DataFrame()
    )
    kh = len(sub)
    act = float(sub['Actual'].sum()) if kh else 0.0
    tgt = float(sub['Target'].sum()) if kh else 0.0
    pct_th = round(act / tgt * 100, 1) if tgt > 0 else 0.0
    pct_kh = round(kh / total_kh * 100, 1) if total_kh else 0.0
    name, bg, color = group_meta[g]
    groups[g] = {
        'name': name,
        'kh': kh,
        'total_kh': total_kh,
        'pct_kh': pct_kh,
        'actual': act,
        'target': tgt,
        'pct_th': pct_th,
        'bg': bg,
        'color': color,
    }

  return {'groups': groups, 'df_detail': df_detail, 'total_kh': total_kh}






# ====================== 14. BÁO CÁO HIỆU SUẤT BÁN HÀNG ======================
def _norm_code(x):
  if pd.isna(x):
    return ''
  s = str(x).strip()
  if s.endswith('.0'):
    s = s[:-2]
  return s


def build_performance_report(
    df_rpt, df_mcp, df_visit, report_date, turnover_targets, filter_nv=None
):
  """Báo cáo Hiệu suất bán hàng — logic theo công thức cột (Call Plan / Fundamental)."""
  title = 'BÁO CÁO HIỆU SUẤT BÁN HÀNG'
  empty = pd.DataFrame()
  try:
    _f4, _f2 = load_dskh_trai_tuyen()
    _perf_dskh_rules = build_dskh_exempt_lookup(_f4, _f2)
  except Exception:
    _perf_dskh_rules = {}

  # MCP: L1 + VIP
  ch_l1, ch_vip = {}, {}
  if df_mcp is not None and not df_mcp.empty:
    c_ma = find_col(df_mcp, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    c_l1 = find_col(df_mcp, ['L1', 'Channel'])
    c_vip = find_col(df_mcp, ['VIP MCH', 'VIP_MCH'])
    if c_ma:
      for _, r in df_mcp.iterrows():
        ma = _norm_code(r[c_ma])
        if not ma or ma.lower() in ('nan', 'none'):
          continue
        if c_l1 and pd.notna(r.get(c_l1)):
          ch_l1[ma] = str(r[c_l1])
        if c_vip and pd.notna(r.get(c_vip)):
          ch_vip[ma] = str(r[c_vip]).strip().upper()

  def _is_on(ma):
    l1 = str(ch_l1.get(_norm_code(ma), '')).lower()
    return ('on' in l1) and ('off' not in l1)

  def _is_vip(ma, nhom=''):
    """VIP3 / VIP5 / VIPSI — map MCP + Tên Nhóm CH trên lịch VT."""
    v = ch_vip.get(_norm_code(ma), '')
    n = str(nhom or '').strip().upper().replace(' ', '')
    return v in ('VIP3', 'VIP5', 'VIPSI') or n in ('VIP3', 'VIP5', 'VIPSI')

  # ----- Lịch VT ngày -----
  vis = pd.DataFrame()
  if df_visit is not None and not df_visit.empty:
    vis = df_visit.copy()
    if '_plan_date' not in vis.columns and 'Ngày lịch VT' in vis.columns:
      vis['_plan_date'] = pd.to_datetime(
          vis['Ngày lịch VT'], dayfirst=True, errors='coerce'
      ).dt.date
    # Ngày VT thực tế (đối chiếu trái tuyến)
    if 'Ngày VT thực tế' in vis.columns:
      vis['_actual'] = pd.to_datetime(
          vis['Ngày VT thực tế'], dayfirst=True, errors='coerce'
      ).dt.date
    elif '_vt_dt' in vis.columns:
      vis['_actual'] = pd.to_datetime(vis['_vt_dt'], errors='coerce').dt.date
    else:
      vis['_actual'] = pd.NaT
    if '_plan_date' in vis.columns:
      rd = report_date.date() if hasattr(report_date, 'date') else report_date
      # Giữ dòng: lịch VT = ngày BC  HOẶC  VT thực tế = ngày BC (trái tuyến)
      mask = vis['_plan_date'] == rd
      if '_actual' in vis.columns:
        mask = mask | (vis['_actual'] == rd)
      vis = vis[mask].copy()

  if not vis.empty:
    vis['_ma'] = vis['Mã Cửa hàng'].map(_norm_code)
    vis['_nv'] = vis['Tên NVBH'].astype(str).str.strip()
    vis['_nv_code'] = vis['Mã NVBH'].map(_norm_code)
    vis['_status'] = vis['Trạng thái'].astype(str).str.strip()
    vis['_nhom'] = (
        vis['Tên Nhóm CH'].astype(str).str.strip()
        if 'Tên Nhóm CH' in vis.columns
        else ''
    )
    vis['_trai'] = (
        vis['VT Trái tuyến'].astype(str).str.strip().str.upper()
        if 'VT Trái tuyến' in vis.columns
        else 'NO'
    )
    # Ngày VT thực tế — đối chiếu PC Trái Tuyến
    if 'Ngày VT thực tế' in vis.columns:
      vis['_actual'] = pd.to_datetime(
          vis['Ngày VT thực tế'], dayfirst=True, errors='coerce'
      ).dt.date
    elif '_vt_dt' in vis.columns:
      vis['_actual'] = pd.to_datetime(vis['_vt_dt'], errors='coerce').dt.date
    else:
      vis['_actual'] = pd.NaT
    # Đã VT = đã check-in (không còn "Chờ viếng thăm")
    vis['_da_vt'] = ~vis['_status'].isin(['Chờ viếng thăm', 'nan', '', 'None'])
    # PC = Có đơn hàng trên file lịch VT
    vis['_co_dh'] = vis['_status'] == 'Có đơn hàng'

  if nv_selected(filter_nv) and not vis.empty:
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    vis = vis[vis['_nv'].isin(vals)]

  # ----- RPT ngày -----
  df_day = pd.DataFrame()
  if df_rpt is not None and not df_rpt.empty and 'date' in df_rpt.columns:
    rd = report_date.date() if hasattr(report_date, 'date') else report_date
    df_day = df_rpt[df_rpt['date'] == rd].copy()
  if nv_selected(filter_nv) and not df_day.empty:
    df_day = filter_df_by_nv(df_day, 'Tên NVBH', filter_nv)

  if not df_day.empty:
    if 'Ngày tạo đơn hàng' in df_day.columns:
      _dt = pd.to_datetime(
          df_day['Ngày tạo đơn hàng'], dayfirst=True, errors='coerce'
      )
      df_day['_hour'] = _dt.dt.hour.fillna(12)
    else:
      df_day['_hour'] = 12
    df_day['_ma'] = df_day['Mã CH'].map(_norm_code)
    df_day['_nv'] = df_day['Tên NVBH'].astype(str).str.strip()
    df_day['_nv_code'] = df_day['Mã NVBH'].map(_norm_code)
    val_col = find_col(
        df_day, ['Thành tiền trước CK', 'Thành tiền trước chiết khấu']
    ) or 'Thành tiền trước CK'
    df_day['_sales'] = (
        pd.to_numeric(df_day[val_col], errors='coerce').fillna(0)
        if val_col in df_day.columns
        else 0
    )
    if 'Tên SP lower' not in df_day.columns:
      sp = (
          df_day['Tên sản phẩm']
          if 'Tên sản phẩm' in df_day.columns
          else ''
      )
      df_day['Tên SP lower'] = (
          pd.Series(sp, index=df_day.index).astype(str).str.lower()
      )
    if 'Mã đơn hàng' not in df_day.columns:
      df_day['Mã đơn hàng'] = df_day.index.astype(str)

  tot_wd, _, _, _ = get_timegone_stats(report_date)
  roster = get_all_sm_roster()

  nv_map = {}
  if not vis.empty:
    for _, r in vis[['_nv', '_nv_code']].drop_duplicates().iterrows():
      if r['_nv'] and r['_nv'].lower() not in ('nan', 'none'):
        nv_map[r['_nv']] = r['_nv_code']
  if not df_day.empty:
    for _, r in df_day[['_nv', '_nv_code']].drop_duplicates().iterrows():
      if r['_nv'] and r['_nv'] not in nv_map:
        nv_map[r['_nv']] = r['_nv_code']
  if not nv_map:
    for code, name in roster.items():
      if name:
        nv_map[name] = code
  if nv_selected(filter_nv):
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    nv_map = {k: v for k, v in nv_map.items() if k in vals}

  # Tập CH nằm trên lịch VT hôm nay (toàn team / đã lọc NV)
  plan_set_all = set(vis['_ma'].tolist()) if not vis.empty else set()

  # --- Kỷ Luật Bán Hàng (TB) ---
  try:
    _df_disp_tb = load_display_data()
  except Exception:
    _df_disp_tb = pd.DataFrame()
  try:
    _df_bohinh = load_bo_hinh_data()
  except Exception:
    _df_bohinh = pd.DataFrame()
  _tb_per_map, _tb_chup_map = build_tb_discipline_maps(
      _df_disp_tb, _df_bohinh, vis, report_date, df_mcp
  )

  rows = []
  for nv_name, nv_code in sorted(nv_map.items(), key=lambda x: x[0]):
    v_nv = vis[vis['_nv'] == nv_name] if not vis.empty else pd.DataFrame()
    d_nv = df_day[df_day['_nv'] == nv_name] if not df_day.empty else pd.DataFrame()
    d_mid = d_nv[d_nv['_hour'] < 13] if not d_nv.empty else pd.DataFrame()

    # ----- Gán theo Ngày VT thực tế / Ngày lịch VT -----
    # Plan VT  : Ngày lịch VT == ngày BC
    # Đã VT    : date(Ngày VT thực tế) == ngày BC
    # PC       : actual == ngày BC + Có đơn hàng + CH NẰM TRONG lịch VT ngày BC
    # PC Trái  : actual == ngày BC + Có đơn hàng + CH KHÔNG nằm trong lịch VT ngày BC
    #            (hoặc VT Trái tuyến = YES)
    # KO ĐH    : actual == ngày BC + đã VT + không có đơn
    rd = report_date.date() if hasattr(report_date, 'date') else report_date

    plan_off, plan_on = set(), set()
    da_off, da_on = set(), set()
    pc_off, pc_on = set(), set()
    trai_off, trai_on = set(), set()
    vip_ko, ko_off, ko_on = set(), set(), set()

    # Tập CH có trên lịch VT đúng ngày BC
    plan_set_all = set()
    if not v_nv.empty and '_plan_date' in v_nv.columns:
      plan_set_all = set(
          m for m in v_nv.loc[v_nv['_plan_date'] == rd, '_ma'].tolist() if m
      )
    elif not v_nv.empty:
      plan_set_all = set(m for m in v_nv['_ma'].tolist() if m)

    if not v_nv.empty:
      # Plan VT theo lịch
      if '_plan_date' in v_nv.columns:
        v_plan = v_nv[v_nv['_plan_date'] == rd]
      else:
        v_plan = v_nv
      for ma in v_plan['_ma'].unique():
        if ma:
          (plan_on if _is_on(ma) else plan_off).add(ma)

      # Lượt VT / ĐH theo Ngày VT thực tế
      if '_actual' in v_nv.columns:
        v_act = v_nv[v_nv['_actual'] == rd].copy()
      else:
        v_act = v_nv.iloc[0:0].copy()

      for _, r in v_act.iterrows():
        ma = r.get('_ma', '')
        if not ma:
          continue
        is_on = _is_on(ma)
        is_trai_flag = str(r.get('_trai', 'NO')).upper() == 'YES'
        co_dh = bool(r.get('_co_dh', False))
        da_vt = bool(r.get('_da_vt', False))
        on_plan = ma in plan_set_all

        # Đã VT (có ngày VT thực tế trong ngày BC)
        if da_vt or co_dh or is_trai_flag:
          (da_on if is_on else da_off).add(ma)

        if co_dh:
          # Trái tuyến: không nằm lịch VT ngày BC, hoặc cờ YES
          # Ngoại lệ: CH trong DSKH F4/F2 đúng lịch VT bổ sung → KHÔNG tính trái tuyến
          if (not on_plan) or is_trai_flag:
            if check_dskh_bo_sung(ma, rd, _perf_dskh_rules):
              (pc_on if is_on else pc_off).add(ma)  # coi như đúng tuyến bổ sung
            else:
              (trai_on if is_on else trai_off).add(ma)
          else:
            # PC đúng tuyến: có ĐH + nằm trong lịch VT ngày BC
            (pc_on if is_on else pc_off).add(ma)
        elif da_vt:
          (ko_on if is_on else ko_off).add(ma)
          if _is_vip(ma, r.get('_nhom', '')):
            vip_ko.add(ma)

      # Bổ sung từ RPT: CH có đơn ngày BC nhưng không có trên lịch VT ngày BC
      if not d_nv.empty:
        for ma in d_nv['_ma'].unique():
          if not ma:
            continue
          if ma not in plan_set_all:
            if check_dskh_bo_sung(ma, rd, _perf_dskh_rules):
              continue  # ngoại lệ DSKH bổ sung
            is_on = _is_on(ma)
            (trai_on if is_on else trai_off).add(ma)

    pct_off = round(len(pc_off) / len(da_off) * 100, 1) if da_off else 0.0
    pct_on = round(len(pc_on) / len(da_on) * 100, 1) if da_on else 0.0

    # LPPC OFF giống KPI: trừ Meat/Beer, line đạt MOQ, PC ≥1 line MOQ, max 1 PC/CH/ngày
    d_off = (
        d_nv[d_nv['_ma'].map(lambda m: not _is_on(m))]
        if not d_nv.empty
        else pd.DataFrame()
    )
    lppc_off = 0.0
    n_dh_off = 0
    n_line_off = 0
    try:
      if not d_off.empty:
        _d = d_off.copy()
        if 'Tên SP lower' not in _d.columns and 'Tên sản phẩm' in _d.columns:
          _d['Tên SP lower'] = _d['Tên sản phẩm'].astype(str).str.lower()
        _sub = _d['Sub Division'].astype(str) if 'Sub Division' in _d.columns else pd.Series('', index=_d.index)
        _name = _d['Tên SP lower'] if 'Tên SP lower' in _d.columns else pd.Series('', index=_d.index)
        _ex = _sub.str.contains(
            'Beer|Bia|Processed Meats|Thịt chế biến', case=False, na=False
        ) | _name.str.contains(
            'beer|bia lush|white lion|red ruby|xúc xích|xuc xich|ponnie|'
            'cao bồi|cao boi|hotdog|thịt viên|chân gà',
            na=False,
        )
        _d = _d[~_ex]
        if not _d.empty:
          order_moq = count_moq_lines_per_order(_d)
          ok = order_moq[order_moq['n_moq_lines'] >= 1]
          ok_day = pick_best_pc_per_outlet_day(ok)
          # chỉ ngày BC
          if 'date' in ok_day.columns:
            ok_day = ok_day[ok_day['date'] == rd]
          n_dh_off = int(len(ok_day))
          n_line_off = int(ok_day['n_moq_lines'].sum()) if n_dh_off else 0
          lppc_off = round(n_line_off / n_dh_off, 2) if n_dh_off else 0.0
    except Exception:
      lppc_off = 0.0
    # PC < 3line OFF: số ĐH kênh OFF có tổng line (SKU unique) < 3
    pc_lt3_off = 0
    if not d_off.empty and 'Mã đơn hàng' in d_off.columns:
      _sku = (
          'Mã sản phẩm' if 'Mã sản phẩm' in d_off.columns
          else ('Tên sản phẩm' if 'Tên sản phẩm' in d_off.columns else None)
      )
      if _sku:
        _lines = d_off.groupby('Mã đơn hàng')[_sku].nunique()
        pc_lt3_off = int((_lines < 3).sum())

    # SellOut
    sm_code = _norm_code(nv_code)
    month_tgt = float(turnover_targets.get(sm_code, 0) or 0)
    if month_tgt == 0:
      for c, n in roster.items():
        if n == nv_name:
          month_tgt = float(turnover_targets.get(c, 0) or 0)
          sm_code = c
          break
    ct_ngay = int(round(month_tgt / tot_wd, 0)) if tot_wd else 0
    th_so = float(d_nv['_sales'].sum()) if not d_nv.empty else 0.0
    th_so_mid = float(d_mid['_sales'].sum()) if not d_mid.empty else 0.0
    pct_so = round(th_so / ct_ngay * 100, 1) if ct_ngay else 0.0
    pct_so_mid = round(th_so_mid / ct_ngay * 100, 1) if ct_ngay else 0.0

    # ASO: số ĐH (Mã đơn hàng) thỏa SP + pattern (MOQ/rule đơn giản: có mua SP)
    def _count_aso_dh(dsub, pattern):
      if dsub is None or dsub.empty or 'Tên SP lower' not in dsub.columns:
        return 0
      m = dsub['Tên SP lower'].astype(str).str.contains(
          pattern, case=False, na=False, regex=True
      )
      if not m.any():
        return 0
      return int(dsub.loc[m, 'Mã đơn hàng'].nunique())

    pat_x = r'búp non|bup non|tea\s*365|tea365|trà.*365'
    pat_v = r'homey.*2\.9|homey.*2,9|giặt xả homey|giat xa homey|homey.*jeju'
    aso_x = _count_aso_dh(d_nv, pat_x)
    aso_x_mid = _count_aso_dh(d_mid, pat_x)
    aso_v = _count_aso_dh(d_nv, pat_v)
    aso_v_mid = _count_aso_dh(d_mid, pat_v)
    ct_x, ct_v = 5, 3

    # Combo OFF/ON theo ngày (cùng rule Báo Cáo ĐH Combo)
    ct_combo_off, ct_combo_on = 5, 3
    th_combo_off, th_combo_on = 0, 0
    try:
      _combo_day = tag_combo_orders_t10(d_nv, mcp_df=df_mcp) if not d_nv.empty else pd.DataFrame()
      if _combo_day is not None and not _combo_day.empty:
        if 'Mã đơn hàng' not in _combo_day.columns:
          for _c in ['Order No', 'OrderNo', 'Số đơn', 'Order ID', 'Mã ĐH', 'Doc No']:
            if _c in _combo_day.columns:
              _combo_day['Mã đơn hàng'] = _combo_day[_c].astype(str)
              break
        if 'channel' not in _combo_day.columns:
          _combo_day['channel'] = 'OFF'
        _ch = _combo_day['channel'].astype(str).str.upper()
        if 'Mã đơn hàng' in _combo_day.columns:
          th_combo_off = int(
              _combo_day.loc[_ch.str.contains('OFF', na=False), 'Mã đơn hàng'].nunique()
          )
          th_combo_on = int(
              _combo_day.loc[
                  _ch.str.contains('ON', na=False) & ~_ch.str.contains('OFF', na=False),
                  'Mã đơn hàng',
              ].nunique()
          )
        else:
          th_combo_off = int((_ch.str.contains('OFF', na=False)).sum())
          th_combo_on = int(
              (_ch.str.contains('ON', na=False) & ~_ch.str.contains('OFF', na=False)).sum()
          )
    except Exception:
      th_combo_off, th_combo_on = 0, 0

    # ----- Chỉ số giữa ngày (RPT < 13h) -----
    d_mid_off = (
        d_mid[d_mid['_ma'].map(lambda m: not _is_on(m))]
        if (not d_mid.empty and '_ma' in d_mid.columns) else pd.DataFrame()
    )
    d_mid_on = (
        d_mid[d_mid['_ma'].map(lambda m: _is_on(m))]
        if (not d_mid.empty and '_ma' in d_mid.columns) else pd.DataFrame()
    )
    pc_off_mid = set(d_mid_off['_ma'].unique()) if not d_mid_off.empty else set()
    pc_on_mid = set(d_mid_on['_ma'].unique()) if not d_mid_on.empty else set()
    pc_off_mid = pc_off_mid & (plan_off | da_off)
    pc_on_mid = pc_on_mid & (plan_on | da_on)
    pct_off_mid = round(len(pc_off_mid) / len(da_off) * 100, 1) if da_off else 0.0
    pct_on_mid = round(len(pc_on_mid) / len(da_on) * 100, 1) if da_on else 0.0
    # LPPC mid-day giống KPI (≥1 MOQ, trừ Meat/Beer)
    lppc_off_mid = 0.0
    n_dh_off_mid = 0
    try:
      if not d_mid_off.empty:
        _dm = d_mid_off.copy()
        if 'Tên SP lower' not in _dm.columns and 'Tên sản phẩm' in _dm.columns:
          _dm['Tên SP lower'] = _dm['Tên sản phẩm'].astype(str).str.lower()
        _sub = _dm['Sub Division'].astype(str) if 'Sub Division' in _dm.columns else pd.Series('', index=_dm.index)
        _name = _dm['Tên SP lower'] if 'Tên SP lower' in _dm.columns else pd.Series('', index=_dm.index)
        _ex = _sub.str.contains(
            'Beer|Bia|Processed Meats|Thịt chế biến', case=False, na=False
        ) | _name.str.contains(
            'beer|bia lush|white lion|red ruby|xúc xích|xuc xich|ponnie|'
            'cao bồi|cao boi|hotdog|thịt viên|chân gà', na=False,
        )
        _dm = _dm[~_ex]
        if not _dm.empty:
          _om = count_moq_lines_per_order(_dm)
          _ok = _om[_om['n_moq_lines'] >= 1]
          _okd = pick_best_pc_per_outlet_day(_ok)
          n_dh_off_mid = int(len(_okd))
          _ln = int(_okd['n_moq_lines'].sum()) if n_dh_off_mid else 0
          lppc_off_mid = round(_ln / n_dh_off_mid, 2) if n_dh_off_mid else 0.0
    except Exception:
      lppc_off_mid = 0.0
      n_dh_off_mid = 0
    ko_off_mid = max(len(da_off) - len(pc_off_mid), 0) if da_off else 0
    ko_on_mid = max(len(da_on) - len(pc_on_mid), 0) if da_on else 0
    pct_x_mid = round(aso_x_mid / ct_x * 100, 1) if ct_x else 0.0
    pct_v_mid = round(aso_v_mid / ct_v * 100, 1) if ct_v else 0.0
    pct_x = round(aso_x / ct_x * 100, 1) if ct_x else 0.0
    pct_v = round(aso_v / ct_v * 100, 1) if ct_v else 0.0

    de_xuat = []
    if ct_ngay and pct_so_mid < 50:
      de_xuat.append('SellOut')
    if pct_x_mid < 50:
      de_xuat.append('ASO Xanh')
    if pct_v_mid < 50:
      de_xuat.append('ASO Vàng')
    if da_off and pct_off_mid < 50:
      de_xuat.append('VT OFF')
    if da_on and pct_on_mid < 50:
      de_xuat.append('VT ON')
    if n_dh_off_mid and lppc_off_mid < 4.3:
      de_xuat.append('LPPC')
    if ko_off_mid > 0:
      de_xuat.append('KO ĐH OFF')
    if ko_on_mid > 0:
      de_xuat.append('KO ĐH ON')
    de_xuat_str = ', '.join(de_xuat) if de_xuat else 'OK'

    def _trend_tag(a, b):
      try:
        a, b = float(a), float(b)
      except Exception:
        return '→Ổn định'
      if a > b:
        return '↑Tăng'
      if a < b:
        return '↓Giảm'
      return '→Ổn định'

    # Gom nhóm: Tăng (chữ xanh đậm) / Ko Tăng|Giảm (chữ đỏ đậm)
    def _tag3(a, b):
      try:
        a, b = float(a), float(b)
      except Exception:
        return 'Ko Tăng'
      if a > b:
        return 'Tăng'
      if a < b:
        return 'Giảm'
      return 'Ko Tăng'

    _pairs = [
        ('SO', _tag3(th_so, th_so_mid)),
        ('VT-OFF', _tag3(pct_off, pct_off_mid)),
        ('VT-ON', _tag3(pct_on, pct_on_mid)),
        ('LPPC', _tag3(lppc_off, lppc_off_mid)),
        ('Xanh', _tag3(aso_x, aso_x_mid)),
        ('Vàng', _tag3(aso_v, aso_v_mid)),
    ]
    _grp = {'Tăng': [], 'Ko Tăng': [], 'Giảm': []}
    for _name, _tg in _pairs:
      _grp[_tg].append(_name)
    _parts = []
    if _grp['Tăng']:
      _parts.append(
          '<span style="color:#228b22;font-weight:800;">'
          + ', '.join(_grp['Tăng']) + ' => Tăng</span>'
      )
    for _lab in ('Ko Tăng', 'Giảm'):
      if _grp[_lab]:
        _parts.append(
            '<span style="color:#c53030;font-weight:800;">'
            + ', '.join(_grp[_lab]) + f' => {_lab}</span>'
        )
    danh_gia = ' | '.join(_parts) if _parts else (
        '<span style="color:#c53030;font-weight:800;">Ko Tăng</span>'
    )
    _delta_so = float(th_so) - float(th_so_mid)
    _delta_x = int(aso_x) - int(aso_x_mid)
    _delta_v = int(aso_v) - int(aso_v_mid)
    _delta_lppc = float(lppc_off) - float(lppc_off_mid)
    _delta_pct_off = float(pct_off) - float(pct_off_mid)
    _delta_pct_on = float(pct_on) - float(pct_on_mid)
    _n_trai = len(trai_off) + len(trai_on)
    _n_vip_ko = len(vip_ko)
    _pct_vt_dh = (
        round(len(pc_off | pc_on) / max(len(da_off | da_on), 1) * 100, 1)
        if (da_off or da_on) else 0.0
    )
    _pct_so = pct_so
    _pct_x = pct_x
    _pct_v = pct_v
    _lppc = float(lppc_off)

    rows.append({
        'Mã NVBH': sm_code,
        'Tên NVBH': nv_name,
        'Plan VT OFF': len(plan_off),
        'Đã VT OFF': len(da_off),
        'PC OFF': len(pc_off),
        'PC < 3line OFF': pc_lt3_off,
        '% PC/VT OFF': f'{pct_off}%',
        'VIP KO ĐH': len(vip_ko),
        'KO ĐH OFF': len(ko_off),
        'PC Trái Tuyến OFF': len(trai_off),
        'Plan VT ON': len(plan_on),
        'Đã VT ON': len(da_on),
        'PC ON': len(pc_on),
        '% PC/Plan ON': f'{pct_on}%',
        'KO ĐH ON': len(ko_on),
        'PC Trái Tuyến ON': len(trai_on),
        'Tổng PC OFF (ĐH)': n_dh_off,
        'LPPC OFF': lppc_off,
        'CT Ngày SO': ct_ngay,
        'TH SO': int(round(th_so, 0)),
        '% TH SO': f'{pct_so}%',
        'CT Xanh': ct_x,
        'TH Xanh': aso_x,
        '% TH Xanh': f'{round(aso_x / ct_x * 100, 1)}%',
        'CT Vàng': ct_v,
        'TH Vàng': aso_v,
        '% TH Vàng': f'{round(aso_v / ct_v * 100, 1)}%',
        'CT Combo OFF': ct_combo_off,
        'TH Combo OFF': th_combo_off,
        '% TH Combo OFF': f'{round(th_combo_off / ct_combo_off * 100, 1) if ct_combo_off else 0}%',
        'CT Combo ON': ct_combo_on,
        'TH Combo ON': th_combo_on,
        '% TH Combo ON': f'{round(th_combo_on / ct_combo_on * 100, 1) if ct_combo_on else 0}%',
        'Số CH TB PER': int(_tb_per_map.get(nv_name, 0) or 0),
        'Chụp hình bởi ĐDKD': int(_tb_chup_map.get(nv_name, 0) or 0),
        '% TH TB': (
            f'{round(int(_tb_chup_map.get(nv_name, 0) or 0) / max(int(_tb_per_map.get(nv_name, 0) or 0), 1) * 100, 1)}%'
            if int(_tb_per_map.get(nv_name, 0) or 0) > 0
            else '0%'
        ),
        'Đề xuất cải thiện': de_xuat_str,
        'Đánh giá Tăng/Giảm': danh_gia,
        '_delta_so': _delta_so,
        '_delta_x': _delta_x,
        '_delta_v': _delta_v,
        '_delta_lppc': _delta_lppc,
        '_delta_pct_off': _delta_pct_off,
        '_delta_pct_on': _delta_pct_on,
        '_n_trai': _n_trai,
        '_n_vip_ko': _n_vip_ko,
        '_pct_vt_dh': _pct_vt_dh,
        '_pct_so': _pct_so,
        '_pct_x': _pct_x,
        '_pct_v': _pct_v,
        '_lppc': _lppc,
        '_sort': pct_so,
    })

  if not rows:
    return empty, title

  df_out = (
      pd.DataFrame(rows)
      .sort_values('_sort')
      .drop(columns=['_sort'])
      .reset_index(drop=True)
  )
  df_out.insert(0, 'STT', range(1, len(df_out) + 1))

  def _sum(c):
    return int(df_out[c].sum()) if c in df_out.columns else 0

  def _avg(c):
    return round(float(df_out[c].mean()), 2) if c in df_out.columns and len(df_out) else 0

  tot_da_off, tot_pc_off = _sum('Đã VT OFF'), _sum('PC OFF')
  tot_da_on, tot_pc_on = _sum('Đã VT ON'), _sum('PC ON')
  tot_ct, tot_th = _sum('CT Ngày SO'), _sum('TH SO')
  tot_cx, tot_tx = _sum('CT Xanh'), _sum('TH Xanh')
  tot_cv, tot_tv = _sum('CT Vàng'), _sum('TH Vàng')
  tot_c_off, tot_th_c_off = _sum('CT Combo OFF'), _sum('TH Combo OFF')
  tot_c_on, tot_th_c_on = _sum('CT Combo ON'), _sum('TH Combo ON')
  total = {
      'STT': '-',
      'Mã NVBH': 'TỔNG CỘNG',
      'Tên NVBH': (
          'SS Trương Thanh Tân Total'
          if not nv_selected(filter_nv)
          else nv_label(filter_nv)
      ),
      'Plan VT OFF': _sum('Plan VT OFF'),
      'Đã VT OFF': tot_da_off,
      'PC OFF': tot_pc_off,
      'PC < 3line OFF': _sum('PC < 3line OFF'),
      '% PC/VT OFF': f'{round(tot_pc_off / tot_da_off * 100, 1) if tot_da_off else 0}%',
      'VIP KO ĐH': _sum('VIP KO ĐH'),
      'KO ĐH OFF': _sum('KO ĐH OFF'),
      'PC Trái Tuyến OFF': _sum('PC Trái Tuyến OFF'),
      'Plan VT ON': _sum('Plan VT ON'),
      'Đã VT ON': tot_da_on,
      'PC ON': tot_pc_on,
      '% PC/Plan ON': f'{round(tot_pc_on / tot_da_on * 100, 1) if tot_da_on else 0}%',
      'KO ĐH ON': _sum('KO ĐH ON'),
      'PC Trái Tuyến ON': _sum('PC Trái Tuyến ON'),
      'Tổng PC OFF (ĐH)': _sum('Tổng PC OFF (ĐH)'),
      'LPPC OFF': _avg('LPPC OFF'),
      'CT Ngày SO': tot_ct,
      'TH SO': tot_th,
      '% TH SO': f'{round(tot_th / tot_ct * 100, 1) if tot_ct else 0}%',
      'CT Xanh': tot_cx,
      'TH Xanh': tot_tx,
      '% TH Xanh': f'{round(tot_tx / tot_cx * 100, 1) if tot_cx else 0}%',
      'CT Vàng': tot_cv,
      'TH Vàng': tot_tv,
      '% TH Vàng': f'{round(tot_tv / tot_cv * 100, 1) if tot_cv else 0}%',
      'CT Combo OFF': tot_c_off,
      'TH Combo OFF': tot_th_c_off,
      '% TH Combo OFF': f'{round(tot_th_c_off / tot_c_off * 100, 1) if tot_c_off else 0}%',
      'CT Combo ON': tot_c_on,
      'TH Combo ON': tot_th_c_on,
      '% TH Combo ON': f'{round(tot_th_c_on / tot_c_on * 100, 1) if tot_c_on else 0}%',
      'Số CH TB PER': _sum('Số CH TB PER'),
      'Chụp hình bởi ĐDKD': _sum('Chụp hình bởi ĐDKD'),
      '% TH TB': (
          f'{round(_sum("Chụp hình bởi ĐDKD") / _sum("Số CH TB PER") * 100, 1)}%'
          if _sum('Số CH TB PER') else '0%'
      ),
      'Đề xuất cải thiện': '',
      'Đánh giá Tăng/Giảm': '',
  }
  df_out = pd.concat([df_out, pd.DataFrame([total])], ignore_index=True)
  return df_out, title


def _perf_table_html(df, section='call'):
  """Format màu giống custom-kpi-table; merge STT/Mã/Tên với header."""
  if df is None or df.empty:
    return '<p>Không có dữ liệu.</p>'

  col_info = ['STT', 'Tên NVBH']
  if section == 'call':
    groups = [
        ('Kênh OFF', [
            ('Plan VT OFF', 'Plan VT'),
            ('Đã VT OFF', 'Đã VT'),
            ('PC OFF', 'PC'),
            ('PC < 3line OFF', 'PC < 3line'),
            ('% PC/VT OFF', '% PC/ VT'),
            ('VIP KO ĐH', 'VIP KO ĐH'),
            ('KO ĐH OFF', 'KO ĐH'),
            ('PC Trái Tuyến OFF', 'PC Trái Tuyến'),
        ]),
        ('Kênh ON', [
            ('Plan VT ON', 'Plan VT'),
            ('Đã VT ON', 'Đã VT'),
            ('PC ON', 'PC'),
            ('% PC/Plan ON', '% PC/Plan'),
            ('KO ĐH ON', 'KO ĐH'),
            ('PC Trái Tuyến ON', 'PC Trái Tuyến'),
        ]),
        ('LPPC', [
            ('Tổng PC OFF (ĐH)', 'Tổng PC OFF'),
            ('LPPC OFF', 'LPPC OFF'),
        ]),
    ]
  else:
    groups = [
        ('SellOut', [
            ('CT Ngày SO', 'CT Ngày'),
            ('TH SO', 'TH'),
            ('% TH SO', '% TH'),
        ]),
        ('ASO Focus Trận Xanh TEA', [
            ('CT Xanh', 'CT Ngày'),
            ('TH Xanh', 'TH'),
            ('% TH Xanh', '% TH'),
        ]),
        ('ASO Focus Trận Vàng Homey 2,9kg', [
            ('CT Vàng', 'CT Ngày'),
            ('TH Vàng', 'TH'),
            ('% TH Vàng', '% TH'),
        ]),
        ('ĐH Combo Kênh OFF', [
            ('CT Combo OFF', 'CT Ngày'),
            ('TH Combo OFF', 'TH'),
            ('% TH Combo OFF', '% TH'),
        ]),
        ('ĐH Combo Kênh ON', [
            ('CT Combo ON', 'CT Ngày'),
            ('TH Combo ON', 'TH'),
            ('% TH Combo ON', '% TH'),
        ]),
        ('Kỷ Luật Bán Hàng', [
            ('Số CH TB PER', 'Số CH TB PER'),
            ('Chụp hình bởi ĐDKD', 'Chụp hình bởi ĐDKD'),
            ('% TH TB', '% TH'),
        ]),
        ('Giữa Ngày', [
            ('Đề xuất cải thiện', 'Đề xuất cải thiện'),
        ]),
        ('Cuối Ngày', [
            ('Đánh giá Tăng/Giảm', 'Đánh Giá Tăng/Giảm'),
        ]),
    ]

  data_cols = [k for _, pairs in groups for k, _ in pairs]
  all_cols = col_info + data_cols

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:bold !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:6px 5px;white-space:nowrap;'
      'font-size:11px;vertical-align:middle;'
  )
  th_top = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:8px;font-size:13px;'
  )
  th_mid = (
      'background-color:#2c5282 !important;color:#ffffff !important;'
      'font-weight:700 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:5px;font-size:11px;'
  )
  td = (
      'border:1px solid #bce2f5 !important;padding:5px 6px;'
      'font-size:11px;white-space:nowrap;'
  )
  # Dòng Total: cùng style header (xanh đậm + trắng) cho cột thường
  td_tot = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;text-align:center !important;'
      'border:1px solid #90cdf4 !important;padding:6px 5px;font-size:11px;'
  )

  n_data = len(data_cols)
  name_w = 150
  try:
    max_len = int(df['Tên NVBH'].astype(str).str.len().max())
    name_w = max(130, min(220, max_len * 8 + 16))
  except Exception:
    pass

  sticky_stt_h = (
      f'{th}position:sticky;left:0;z-index:6;min-width:44px;max-width:44px;'
  )
  sticky_ten_h = (
      f'{th}position:sticky;left:44px;z-index:6;min-width:{name_w}px;'
  )
  sticky_stt_c = 'position:sticky;left:0;z-index:2;min-width:44px;max-width:44px;'
  sticky_ten_c = f'position:sticky;left:44px;z-index:2;min-width:{name_w}px;'

  html = [
      '<div style="overflow-x:auto;margin-bottom:16px;-webkit-overflow-scrolling:touch;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;'
      'width:max-content;min-width:100%;">',
      '<thead style="position:sticky;top:0;z-index:5;">',
  ]

  # Row 1: STT/Tên rowspan=3 + top group titles
  html.append('<tr>')
  html.append(f'<th rowspan="3" style="{sticky_stt_h}">STT</th>')
  html.append(f'<th rowspan="3" style="{sticky_ten_h}">Tên NVBH</th>')
  if section == 'call':
    html.append(f'<th colspan="{n_data}" style="{th_top}">Call Plan</th>')
  else:
    # Fundamental = SellOut + ASO Xanh + ASO Vàng + Combo OFF/ON (15)
    # Kỷ Luật Bán Hàng: rowspan=2 gộp 2 dòng tiêu đề thành 1 ô
    # Đề xuất & Đánh Giá = Giữa + Cuối (2)
    html.append(f'<th colspan="15" style="{th_top}">Fundamental</th>')
    html.append(
        f'<th colspan="3" rowspan="2" style="{th_top}">Kỷ Luật Bán Hàng</th>'
    )
    html.append(f'<th colspan="2" style="{th_top}">Đề xuất &amp; Đánh Giá</th>')
  html.append('</tr>')

  # Row 2: sub-groups — bỏ "Kỷ Luật Bán Hàng" (đã rowspan từ row 1)
  html.append('<tr>')
  for gname, pairs in groups:
    if section != 'call' and gname == 'Kỷ Luật Bán Hàng':
      continue
    html.append(f'<th colspan="{len(pairs)}" style="{th_mid}">{gname}</th>')
  html.append('</tr>')

  # Row 3: leaf headers
  html.append('<tr>')
  for _, pairs in groups:
    for _, lab in pairs:
      extra = 'color:#fc8181 !important;' if lab == 'VIP KO ĐH' else ''
      html.append(f'<th style="{th}{extra}">{lab}</th>')
  html.append('</tr></thead><tbody>')

  # Cột số liệu cần canh giữa
  _center_cols = set(data_cols) | {'STT'}

  n_rows = len(df)
  for pos, (idx, row) in enumerate(df.iterrows()):
    _ma_nv = str(row.get('Mã NVBH', '')).upper()
    _ten_nv = str(row.get('Tên NVBH', '')).upper()
    _stt = str(row.get('STT', '')).strip()
    is_tot = (
        pos == n_rows - 1
        or _stt in ('-', 'TOTAL')
        or 'TỔNG' in _ma_nv
        or 'TOTAL' in _ten_nv
        or 'TỔNG CỘNG' in _ma_nv
    )
    row_bg = ''
    if not is_tot:
      row_bg = (
          'background-color:#e6f4fc !important;'
          if pos % 2 == 0
          else 'background-color:#ffffff !important;'
      )
    else:
      # Total: nền xanh đậm
      row_bg = 'background-color:#1a365d !important;color:#ffffff !important;'

    if is_tot:
      html.append(
          '<tr class="row-total" style="background-color:#1a365d !important;">'
      )
    else:
      html.append('<tr>')
    for c in all_cols:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      if c in ('TH SO', 'CT Ngày SO') and val != '' and val is not None:
        try:
          _n = int(float(str(val).replace('.', '').replace(',', '')))
          val = f'{_n:,}'.replace(',', '.')
        except Exception:
          try:
            val = f'{int(float(val)):,}'.replace(',', '.')
          except Exception:
            pass

      is_pct = isinstance(val, str) and '%' in str(val)
      is_vip_col = c == 'VIP KO ĐH'
      is_danh_gia = (
          ('đánh giá' in str(c).lower())
          or (c == 'Đánh giá Tăng/Giảm')
      )
      is_de_xuat = c == 'Đề xuất cải thiện'
      sticky = ''
      if c == 'STT':
        sticky = sticky_stt_c
      elif c == 'Tên NVBH':
        sticky = sticky_ten_c
      align = 'left' if c == 'Tên NVBH' else 'center'
      sticky_bg = (
          'background-color:#1a365d !important;color:#ffffff !important;'
          if is_tot
          else row_bg
      )

      # Sticky STT / Tên NVBH
      if c in ('STT', 'Tên NVBH'):
        html.append(
            f'<td align="{align}" style="{td}{sticky}{sticky_bg}'
            f'font-weight:{"900" if is_tot else "600"} !important;'
            f'text-align:{align} !important;">{val if str(val).strip() not in ("", "nan", "None") else "&nbsp;"}</td>'
        )
        continue

      # Dòng TOTAL: nền xanh đậm + chữ trắng; cột % vẫn tô màu rule KPI
      if is_tot and is_pct:
        html.append(
            f'<td align="center" data-colored="1" class="{color_pct_class(val)}" '
            f'style="{td}{color_pct_bg(val)}font-weight:900 !important;'
            f'text-align:center !important;">{val}</td>'
        )
      elif is_tot:
        html.append(
            f'<td align="center" data-colored="1" class="row-total-cell" '
            f'style="{td}background-color:#1a365d !important;color:#ffffff !important;'
            f'font-weight:900 !important;text-align:center !important;'
            f'border-color:#1a365d !important;">'
            f'{val if str(val).strip() not in ("", "nan", "None") else "&nbsp;"}</td>'
        )
      elif is_danh_gia:
        zebra_bg = '#e6f4fc' if (pos % 2 == 1) else '#ffffff'
        html.append(
            f'<td align="center" '
            f'style="{td}background-color:{zebra_bg} !important;'
            f'text-align:center !important;font-size:11px;">{val}</td>'
        )
      elif is_pct:
        cls = color_pct_class(val)
        html.append(
            f'<td align="center" data-colored="1" class="{cls}" '
            f'style="{td}{color_pct_bg(val)}text-align:center !important;">{val}</td>'
        )
      elif is_vip_col:
        cls = vip_ko_class(val)
        attr = ' data-colored="1"' if cls else ''
        cls_attr = f' class="{cls}"' if cls else ''
        html.append(
            f'<td align="center"{attr}{cls_attr} '
            f'style="{td}{vip_ko_bg(val)}text-align:center !important;">{val}</td>'
        )
      else:
        html.append(
            f'<td align="center" style="{td}{row_bg}'
            f'text-align:center !important;">{val}</td>'
        )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)




def load_dskh_trai_tuyen():
  """Load DSKH Trái Tuyến — hỗ trợ sheet Import / F4 / F2 / sheet đầu."""
  import unicodedata
  empty = pd.DataFrame()

  def _fold(s):
    s = unicodedata.normalize('NFKD', str(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace('đ', 'd')
    return s

  candidates = []
  search_roots = []
  for d in [DATA_DIR, 'data', '.', '/mount/src', '/mount/src/dashboard-test',
            '/mount/src/dashboard-test/data']:
    if os.path.isdir(d) and d not in search_roots:
      search_roots.append(d)

  for root in search_roots:
    try:
      for dirpath, _, files in os.walk(root):
        if dirpath[len(root):].count(os.sep) > 2:
          continue
        for fn in files:
          if not fn.lower().endswith(('.xlsx', '.xls', '.xlsm')):
            continue
          if 'dskh' in _fold(fn):
            candidates.append(os.path.join(dirpath, fn))
    except Exception:
      continue

  preferred, other = [], []
  for p in candidates:
    f = _fold(os.path.basename(p))
    (preferred if ('trai' in f or 'tuyen' in f) else other).append(p)
  ordered = preferred + other

  path_use = next((p for p in ordered if os.path.isfile(p)), None)
  if not path_use:
    return empty, empty

  try:
    xl = pd.ExcelFile(path_use)
    names = list(xl.sheet_names)
    # Ưu tiên: Import → F4 → F2 → sheet đầu
    pick = None
    for prefer in ['IMPORT', 'F4', 'F2']:
      for s in names:
        if str(s).strip().upper().startswith(prefer):
          pick = s
          break
      if pick:
        break
    if pick is None and names:
      pick = names[0]

    df_all = pd.read_excel(path_use, sheet_name=pick)
    df_all.columns = [str(c).strip() for c in df_all.columns]

    # Tách F4/F2 nếu có 2 sheet riêng; không thì dùng chung 1 df
    s_f4 = s_f2 = None
    for s in names:
      su = str(s).strip().upper()
      if su == 'F4' or su.startswith('F4'):
        s_f4 = s
      if su == 'F2' or su.startswith('F2'):
        s_f2 = s

    if s_f4 or s_f2:
      df_f4 = pd.read_excel(path_use, sheet_name=s_f4) if s_f4 else empty
      df_f2 = pd.read_excel(path_use, sheet_name=s_f2) if s_f2 else empty
      if not df_f4.empty:
        df_f4.columns = [str(c).strip() for c in df_f4.columns]
      if not df_f2.empty:
        df_f2.columns = [str(c).strip() for c in df_f2.columns]
      return df_f4, df_f2

    # 1 sheet (Import): trả về (df, empty) — build_lookup đọc cả 2
    return df_all, empty
  except Exception:
    return empty, empty



def _norm_ma_kh(x):
  """Chuẩn hoá Mã KH: bỏ .0, khoảng trắng, leading zeros không bắt buộc."""
  if x is None or (isinstance(x, float) and pd.isna(x)):
    return ''
  try:
    if isinstance(x, (int, float)) and float(x) == int(float(x)):
      return str(int(float(x)))
  except Exception:
    pass
  s = str(x).strip()
  if s.lower() in ('nan', 'none', ''):
    return ''
  if s.endswith('.0'):
    s = s[:-2]
  # bỏ dấu phẩy ngăn cách
  s = s.replace(',', '').replace(' ', '')
  try:
    if float(s) == int(float(s)):
      return str(int(float(s)))
  except Exception:
    pass
  return s


def _parse_weekday_codes(raw):
  """
  Map NGÀY VT KO TÍNH TRÁI TUYẾN → weekday Python (Mon=0 .. Sun=6).

  Rule cứng theo nghiệp vụ:
    25 → Thứ 2 & Thứ 5  → {0, 3}
    36 → Thứ 3 & Thứ 6  → {1, 4}
    47 → Thứ 4 & Thứ 7  → {2, 5}
  Ngoài ra: T2..T7, 2..7
  """
  if raw is None or (isinstance(raw, float) and pd.isna(raw)):
    return set()
  # Excel số 25 / 25.0 / "25"
  try:
    if isinstance(raw, (int, float)):
      n = int(float(raw))
      if n == 25:
        return {0, 3}
      if n == 36:
        return {1, 4}
      if n == 47:
        return {2, 5}
      if n in (2, 3, 4, 5, 6, 7):
        return {n - 2}  # T2→0 ... T7→5
  except Exception:
    pass

  s = str(raw).strip().upper().replace(' ', '').replace('.0', '')
  if s in ('25', '2&5', '2-5', '2/5'):
    return {0, 3}
  if s in ('36', '3&6', '3-6', '3/6'):
    return {1, 4}
  if s in ('47', '4&7', '4-7', '4/7'):
    return {2, 5}

  mapping = {
      'T2': 0, 'T3': 1, 'T4': 2, 'T5': 3, 'T6': 4, 'T7': 5,
      '2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5,
  }
  if s in mapping:
    return {mapping[s]}
  import re as _re
  out = set()
  for m in _re.findall(r'T([2-7])', s):
    out.add(int(m) - 2)
  return out


def _week_ok(tuan_hien_tai, report_date):
  """Even Week / Odd Week / Both — mặc định True nếu không rõ."""
  if tuan_hien_tai is None or (isinstance(tuan_hien_tai, float) and pd.isna(tuan_hien_tai)):
    return True
  s = str(tuan_hien_tai).strip().lower()
  if not s or 'both' in s or 'cả' in s:
    return True
  try:
    iso = report_date.isocalendar()[1]
  except Exception:
    try:
      iso = pd.Timestamp(report_date).isocalendar()[1]
    except Exception:
      return True
  is_even = iso % 2 == 0
  if 'even' in s or 'chẵn' in s or 'chan' in s:
    return is_even
  if 'odd' in s or 'lẻ' in s:
    return not is_even
  return True


def build_dskh_exempt_lookup(df_f4, df_f2):
  """Map Mã KH → list {days, week, sheet}.

  CHỈ lấy cột NGÀY VT KO TÍNH TRÁI TUYẾN (không lấy Ngày VT bổ sung).
  """
  rules = {}

  def _find_exact(df, *cands):
    cols = {str(c).strip(): c for c in df.columns}
    cols_l = {str(c).strip().lower(): c for c in df.columns}
    for cand in cands:
      if cand in cols:
        return cols[cand]
      cl = cand.lower()
      if cl in cols_l:
        return cols_l[cl]
    # partial: phải chứa đủ cụm "ko tính trái" hoặc "ko tinh trai"
    for k, orig in cols_l.items():
      k2 = (
          k.replace('ế', 'e').replace('é', 'e').replace('á', 'a')
          .replace('à', 'a').replace('ả', 'a').replace('ã', 'a')
          .replace('ạ', 'a').replace('í', 'i').replace('ì', 'i')
          .replace('ỉ', 'i').replace('ĩ', 'i').replace('ị', 'i')
          .replace('ú', 'u').replace('ù', 'u').replace('ủ', 'u')
          .replace('ũ', 'u').replace('ụ', 'u').replace('ư', 'u')
          .replace('ớ', 'o').replace('ờ', 'o').replace('ở', 'o')
          .replace('ỡ', 'o').replace('ợ', 'o').replace('ố', 'o')
          .replace('ồ', 'o').replace('ổ', 'o').replace('ỗ', 'o')
          .replace('ộ', 'o').replace('ó', 'o').replace('ò', 'o')
          .replace('ỏ', 'o').replace('õ', 'o').replace('ọ', 'o')
          .replace('đ', 'd')
      )
      if 'ko tinh trai' in k2 or 'khong tinh trai' in k2:
        return orig
    return None

  def _find_ma(df):
    for cand in ['Mã KH', 'Ma KH', 'Mã CH', 'Ma CH', 'Outlet Code']:
      for c in df.columns:
        if str(c).strip().lower() == cand.lower():
          return c
    for c in df.columns:
      cl = str(c).strip().lower()
      if 'ma' in cl and ('kh' in cl or 'ch' in cl or 'outlet' in cl):
        return c
    return None

  for sheet_name, df in [('F4', df_f4), ('F2', df_f2)]:
    if df is None or df.empty:
      continue
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    c_ma = _find_ma(df)
    c_ngay = _find_exact(
        df,
        'NGÀY VT KO TÍNH TRÁI TUYẾN',
        'NGÀY KO TÍNH TRÁI TUYẾN',
        'Ngày VT KO TÍNH TRÁI TUYẾN',
        'Ngày KO TÍNH TRÁI TUYẾN',
        'NGAY VT KO TINH TRAI TUYEN',
    )
    if c_ngay is None:
      # fallback: cột chứa "trai tuyen" hoặc đúng 1 cột số thứ
      for c in df.columns:
        cl = str(c).strip().lower()
        if 'trai' in cl and ('vt' in cl or 'ngay' in cl or 'ngày' in cl):
          c_ngay = c
          break
    c_tuan = None
    for c in df.columns:
      cl = str(c).strip().lower()
      if 'tuần hiện tại' in cl or 'tuan hien tai' in cl:
        c_tuan = c
        break

    if not c_ma or not c_ngay:
      continue

    for _, r in df.iterrows():
      ma = _norm_ma_kh(r[c_ma])
      if not ma:
        continue
      days = _parse_weekday_codes(r[c_ngay])
      if not days:
        # thử parse lại từ string thô
        days = _parse_weekday_codes(str(r[c_ngay]).strip())
      if not days:
        continue
      tuan = r[c_tuan] if c_tuan is not None else 'Both'
      entry = {
          'days': days,
          'week': tuan,
          'sheet': sheet_name,
      }
      rules.setdefault(ma, []).append(entry)
      # alias key dạng raw
      raw = str(r[c_ma]).strip()
      if raw.endswith('.0'):
        raw = raw[:-2]
      if raw and raw != ma:
        rules.setdefault(raw, []).append(entry)
  return rules


def check_dskh_bo_sung(ma_kh, report_date, rules_lookup):
  """✓ nếu Mã KH trong DSKH và thứ ngày BC khớp NGÀY VT KO TÍNH TRÁI TUYẾN.

  Chỉ check THỨ (25/36/47/2-7). Không filter Even/Odd Week.
  """
  if not rules_lookup:
    return False
  ma = _norm_ma_kh(ma_kh)
  if not ma:
    return False

  candidates = {ma}
  try:
    candidates.add(str(int(float(ma))))
  except Exception:
    pass
  if ma.lstrip('0') and ma.lstrip('0') != ma:
    candidates.add(ma.lstrip('0'))

  matched = None
  for c in candidates:
    if c in rules_lookup:
      matched = rules_lookup[c]
      break
  # fallback: so khớp mọi key đã normalize
  if not matched:
    for k, v in rules_lookup.items():
      if _norm_ma_kh(k) in candidates:
        matched = v
        break
  if not matched:
    return False

  try:
    wd = pd.Timestamp(report_date).weekday()  # Mon=0
  except Exception:
    return False

  for rule in matched:
    days = rule.get('days') or set()
    if wd in days:
      return True
  return False



def build_trai_tuyen_orders(df_rpt, df_visit, df_mcp, report_date, filter_nv=None):
  """Chi tiết ĐH Trái Tuyến.

  Rule:
  1. Lấy CH có Đơn Hàng theo Ngày VT thực tế = ngày BC (file lịch).
  2. Đối chiếu: CH đó có nằm trong lịch VT (Ngày lịch VT = ngày BC) hay không.
  3. Không nằm lịch VT ngày BC → ĐH Trái Tuyến.
  4. Map RPT_061 lấy Mã ĐH, Doanh số, LPPC.
  """
  empty = pd.DataFrame(columns=[
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'Giá trị ĐH [Doanh Số]', 'Ngày ĐH', 'LPPC',
      'Check Lịch VT', 'Check Danh Sách bổ sung',
  ])
  if df_visit is None or df_visit.empty:
    return empty

  # Load DSKH F4/F2 — ngoại lệ trái tuyến
  _dskh_rules = {}
  try:
    _df_f4, _df_f2 = load_dskh_trai_tuyen()
    _dskh_rules = build_dskh_exempt_lookup(_df_f4, _df_f2)
  except Exception:
    _dskh_rules = {}

  rd = report_date.date() if hasattr(report_date, 'date') else report_date
  vis = df_visit.copy()

  # Parse
  if 'Ngày VT thực tế' in vis.columns:
    vis['_actual'] = pd.to_datetime(
        vis['Ngày VT thực tế'], dayfirst=True, errors='coerce'
    ).dt.date
  elif '_actual' not in vis.columns:
    return empty

  if 'Ngày lịch VT' in vis.columns:
    vis['_plan_date'] = pd.to_datetime(
        vis['Ngày lịch VT'], dayfirst=True, errors='coerce'
    ).dt.date
  elif '_plan_date' not in vis.columns:
    vis['_plan_date'] = pd.NaT

  vis['_status'] = (
      vis['Trạng thái'].astype(str).str.strip()
      if 'Trạng thái' in vis.columns
      else ''
  )
  vis['_trai'] = (
      vis['VT Trái tuyến'].astype(str).str.strip().str.upper()
      if 'VT Trái tuyến' in vis.columns
      else 'NO'
  )
  vis['_ma'] = vis['Mã Cửa hàng'].map(
      lambda x: str(x).strip()[:-2] if str(x).endswith('.0') else str(x).strip()
  ) if 'Mã Cửa hàng' in vis.columns else ''
  vis['_nv'] = (
      vis['Tên NVBH'].astype(str).str.strip()
      if 'Tên NVBH' in vis.columns
      else ''
  )

  # Tập CH nằm đúng lịch VT ngày BC
  plan_set = set(
      m for m in vis.loc[vis['_plan_date'] == rd, '_ma'].tolist() if m
  )

  # CH có ĐH theo Ngày VT thực tế = ngày BC
  co_dh_actual = vis[
      (vis['_actual'] == rd) & (vis['_status'] == 'Có đơn hàng')
  ].copy()

  # Trái tuyến = có ĐH (actual=rd) nhưng KHÔNG nằm lịch VT ngày BC
  # hoặc cờ VT Trái tuyến = YES
  trai = co_dh_actual[
      (~co_dh_actual['_ma'].isin(plan_set)) | (co_dh_actual['_trai'] == 'YES')
  ].copy()

  # Bổ sung từ RPT: CH có đơn ngày BC, không có trên lịch VT ngày BC
  trai_ma = set(m for m in trai['_ma'].tolist() if m)
  ch_nv = {}
  if not trai.empty:
    ch_nv = dict(zip(trai['_ma'], trai['_nv']))
  ch_ten = {}
  if 'Tên Cửa hàng' in vis.columns and not trai.empty:
    ch_ten = dict(zip(trai['_ma'], trai['Tên Cửa hàng'].astype(str)))

  if df_rpt is not None and not df_rpt.empty and 'date' in df_rpt.columns:
    d0 = df_rpt[df_rpt['date'] == rd].copy()
    if not d0.empty and 'Mã CH' in d0.columns:
      d0['_ma'] = d0['Mã CH'].map(
          lambda x: str(x).strip()[:-2] if str(x).endswith('.0') else str(x).strip()
      )
      for ma in d0['_ma'].unique():
        if ma and ma not in plan_set:
          trai_ma.add(ma)
          if ma not in ch_nv and 'Tên NVBH' in d0.columns:
            sub = d0[d0['_ma'] == ma]
            ch_nv[ma] = str(sub['Tên NVBH'].iloc[0]).strip() if len(sub) else ''

  if nv_selected(filter_nv):
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    # lọc theo NV sau
    pass

  if not trai_ma:
    return empty

  # Chi tiết từ RPT
  if df_rpt is None or df_rpt.empty or 'date' not in df_rpt.columns:
    rows = []
    for i, ma in enumerate(sorted(trai_ma), 1):
      rows.append({
          'STT': i,
          'Tên NVBH': ch_nv.get(ma, ''),
          'Mã KH': ma,
          'Tên KH': ch_ten.get(ma, ''),
          'Mã ĐH': '',
          'Giá trị ĐH [Doanh Số]': '',
          'Ngày ĐH': rd.strftime('%d/%m/%Y') if hasattr(rd, 'strftime') else str(rd),
          'LPPC': '',
          'Check Lịch VT': 'Không có trên lịch VT',
                })
    out = pd.DataFrame(rows)
    if not out.empty and 'Mã KH' in out.columns:
      out['Check Danh Sách bổ sung'] = out['Mã KH'].map(
          lambda m: '✓' if check_dskh_bo_sung(m, rd, _dskh_rules) else ''
      )
    if nv_selected(filter_nv):
      vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
      out = out[out['Tên NVBH'].isin(vals)]
    return out if not out.empty else empty

  d = df_rpt[df_rpt['date'] == rd].copy()
  d['_ma'] = d['Mã CH'].map(
      lambda x: str(x).strip()[:-2] if str(x).endswith('.0') else str(x).strip()
  )
  d = d[d['_ma'].isin(trai_ma)]
  if d.empty:
    rows = []
    for i, ma in enumerate(sorted(trai_ma), 1):
      rows.append({
          'STT': i,
          'Tên NVBH': ch_nv.get(ma, ''),
          'Mã KH': ma,
          'Tên KH': ch_ten.get(ma, ''),
          'Mã ĐH': '',
          'Giá trị ĐH [Doanh Số]': '',
          'Ngày ĐH': rd.strftime('%d/%m/%Y') if hasattr(rd, 'strftime') else str(rd),
          'LPPC': '',
          'Check Lịch VT': 'Không có trên lịch VT',
                })
    out = pd.DataFrame(rows)
    if not out.empty and 'Mã KH' in out.columns:
      out['Check Danh Sách bổ sung'] = out['Mã KH'].map(
          lambda m: '✓' if check_dskh_bo_sung(m, rd, _dskh_rules) else ''
      )
    if nv_selected(filter_nv):
      vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
      out = out[out['Tên NVBH'].isin(vals)]
    return out if not out.empty else empty

  val_col = find_col(d, ['Thành tiền trước CK', 'Thành tiền trước chiết khấu']) or 'Thành tiền trước CK'
  if val_col not in d.columns:
    d['_sales'] = 0
  else:
    d['_sales'] = pd.to_numeric(d[val_col], errors='coerce').fillna(0)

  ten_kh_col = find_col(d, ['Tên CH', 'Tên khách hàng', 'Tên Cửa hàng']) or 'Tên CH'
  order_col = 'Mã đơn hàng' if 'Mã đơn hàng' in d.columns else None

  rows = []
  if order_col:
    for (ma_dh, ma_kh), g in d.groupby([order_col, '_ma']):
      sales = float(g['_sales'].sum())
      n_lines = len(g)
      nv = ch_nv.get(ma_kh, g['Tên NVBH'].iloc[0] if 'Tên NVBH' in g.columns else '')
      ten_kh = g[ten_kh_col].iloc[0] if ten_kh_col in g.columns else ch_ten.get(ma_kh, '')
      if 'Ngày tạo đơn hàng' in g.columns:
        ngay = pd.to_datetime(g['Ngày tạo đơn hàng'].iloc[0], dayfirst=True, errors='coerce')
        ngay_s = ngay.strftime('%d/%m/%Y %H:%M') if pd.notna(ngay) else str(rd)
      else:
        ngay_s = rd.strftime('%d/%m/%Y') if hasattr(rd, 'strftime') else str(rd)
      rows.append({
          'STT': 0,
          'Tên NVBH': nv,
          'Mã KH': ma_kh,
          'Tên KH': ten_kh,
          'Mã ĐH': ma_dh,
          'Giá trị ĐH [Doanh Số]': int(round(sales, 0)),
          'Ngày ĐH': ngay_s,
          'LPPC': n_lines,
          'Check Lịch VT': 'Không có trên lịch VT',
                })
  else:
    for ma_kh, g in d.groupby('_ma'):
      sales = float(g['_sales'].sum())
      nv = ch_nv.get(ma_kh, '')
      ten_kh = g[ten_kh_col].iloc[0] if ten_kh_col in g.columns else ch_ten.get(ma_kh, '')
      rows.append({
          'STT': 0,
          'Tên NVBH': nv,
          'Mã KH': ma_kh,
          'Tên KH': ten_kh,
          'Mã ĐH': '',
          'Giá trị ĐH [Doanh Số]': int(round(sales, 0)),
          'Ngày ĐH': rd.strftime('%d/%m/%Y') if hasattr(rd, 'strftime') else str(rd),
          'LPPC': len(g),
          'Check Lịch VT': 'Không có trên lịch VT',
                })

  if not rows:
    return empty
  out = pd.DataFrame(rows).sort_values(['Tên NVBH', 'Mã KH', 'Mã ĐH']).reset_index(drop=True)
  if nv_selected(filter_nv):
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    out = out[out['Tên NVBH'].isin(vals)].reset_index(drop=True)
  if out.empty:
    return empty
  out['STT'] = range(1, len(out) + 1)
  out['Giá trị ĐH [Doanh Số]'] = out['Giá trị ĐH [Doanh Số]'].apply(
      lambda x: f'{int(x):,}'.replace(',', '.') if isinstance(x, (int, float)) else x
  )
  # Check Danh Sách bổ sung (F4/F2) — luôn reload để tránh cache rỗng
  try:
    try:
      load_dskh_trai_tuyen.clear()
    except Exception:
      pass
    _df_f4, _df_f2 = load_dskh_trai_tuyen()
    _dskh_rules = build_dskh_exempt_lookup(_df_f4, _df_f2)
  except Exception:
    _dskh_rules = _dskh_rules if _dskh_rules else {}

  # Precompute set Mã KH được tick hôm nay (thứ khớp 25/36/47)
  try:
    _wd = pd.Timestamp(rd).weekday()  # Mon=0 .. Sat=5
  except Exception:
    _wd = -1
  _tick_mas = set()
  for _ma, _rules in (_dskh_rules or {}).items():
    for _r in _rules:
      if _wd in (_r.get('days') or set()) and _week_ok(_r.get('week'), rd):
        _tick_mas.add(str(_ma))
        try:
          _tick_mas.add(str(int(float(_ma))))
        except Exception:
          pass

  def _chk_bs(ma):
    s = str(ma).strip()
    if s.endswith('.0'):
      s = s[:-2]
    if s in _tick_mas:
      return '✓'
    try:
      if str(int(float(s))) in _tick_mas:
        return '✓'
    except Exception:
      pass
    return ''
  out['Check Danh Sách bổ sung'] = out['Mã KH'].map(_chk_bs)
  return out



# ====================== 15. BÁO CÁO TRƯNG BÀY ======================
@st.cache_data(ttl=120, show_spinner=False)
# ====================== 16. KẾ HOẠCH TÁC CHIẾN TRÀ BÚP NON ======================
def _resolve_raw_tea_path():
  """Ưu tiên data.xlsx (RR 3 tháng Bev/Tea), sau đó RAW DATA.*"""
  names = [
      'data.xlsx', 'Data.xlsx', 'DATA.xlsx',
      'RAW DATA.xlsx', 'RAW_DATA.xlsx', 'Raw Data.xlsx',
      'RAW DATA.xls', 'Data_RAW_TEA.xlsx',
  ]
  for n in names:
    p = os.path.join(get_data_dir(), n)
    if os.path.isfile(p):
      return p
  if os.path.isdir(get_data_dir()):
    scored = []
    for fn in os.listdir(get_data_dir()):
      if not fn.lower().endswith(('.xlsx', '.xls')):
        continue
      low = fn.lower().replace(' ', '').replace('_', '')
      # data.xlsx kiểu export PowerBI / OneTech
      if low in ('data.xlsx', 'data.xls'):
        scored.append((0, fn))
      elif 'rawdata' in low or (low.startswith('raw') and 'data' in low):
        scored.append((1, fn))
    scored.sort()
    if scored:
      return os.path.join(get_data_dir(), scored[0][1])
  return os.path.join(get_data_dir(), 'data.xlsx')


def _resolve_dk_tea_path():
  if not os.path.isdir(get_data_dir()):
    return None
  keys = ('tichluy', 'tích lũy', 'dangky', 'đăng ký', 'msc_bev', 'bupnon', 'búp non', 'tea365')
  for fn in os.listdir(get_data_dir()):
    if not fn.lower().endswith(('.xlsx', '.xls')):
      continue
    low = fn.lower()
    if any(k in low for k in keys) and 'raw' not in low.replace(' ', ''):
      return os.path.join(get_data_dir(), fn)
  return None


@st.cache_data(ttl=600)
def load_raw_tea_data():
  path = _resolve_raw_tea_path()
  if not os.path.isfile(path):
    return pd.DataFrame()
  raw = pd.read_excel(path, header=None, dtype=object)
  header_row = None
  markers = ('outlet_code', 'outlet code', 'sm_name', 'order_dt', 'order date', 'brand_desc', 'brand')
  for i in range(min(10, len(raw))):
    vals = [str(x).strip().lower() for x in raw.iloc[i].tolist() if pd.notna(x)]
    joined = ' | '.join(vals)
    if sum(1 for m in markers if m in joined) >= 3:
      header_row = i
      break
  if header_row is None:
    header_row = 2
  cols = [str(c).strip() if pd.notna(c) else f'Col_{i}' for i, c in enumerate(raw.iloc[header_row].tolist())]
  df = raw.iloc[header_row + 1:].copy()
  df.columns = cols
  df = df.dropna(how='all')
  return df.reset_index(drop=True)


@st.cache_data(ttl=600)
def load_dk_tea_outlets():
  """CH đã ĐK chương trình Tích Lũy Trà Búp Non Tea 365 (MSC_BEV ... T10).

  Ưu tiên file DANH_SACH_KET_QUA... (cùng file trưng bày), lọc đúng tên CT.
  """
  paths = []
  p1 = _resolve_dk_tea_path()
  if p1:
    paths.append(p1)
  # Cùng file trưng bày
  for n in [
      'DANH_SACH_KET_QUA_CUA_HANG_THAM_GIA_CHUONG_TRINH.xlsx',
      'DANH_SACH_KET_QUA_CUA_HANG_THAM_GIA_CHUONG_TRINH.xls',
  ]:
    p = os.path.join(get_data_dir(), n)
    if os.path.isfile(p) and p not in paths:
      paths.append(p)
  if os.path.isdir(get_data_dir()):
    for fn in os.listdir(get_data_dir()):
      if 'ket_qua' in fn.lower().replace(' ', '') or 'thamgiachuongtrinh' in fn.lower().replace(' ', ''):
        p = os.path.join(get_data_dir(), fn)
        if p not in paths:
          paths.append(p)

  PROG_KEY = 'tích lũy'
  PROG_KEY2 = 'tich luy'
  PROG_TEA = 'búp non'
  PROG_TEA2 = 'bup non'
  PROG_TEA3 = 'tea 365'

  for path in paths:
    try:
      raw = pd.read_excel(path, header=None, dtype=object)
      header_row = 0
      for i in range(min(15, len(raw))):
        vals = [str(x).strip().lower() for x in raw.iloc[i].tolist() if pd.notna(x)]
        joined = ' | '.join(vals)
        if any(k in joined for k in ('mã ch', 'ma ch', 'mã kh', 'tên chương trình', 'ten chuong trinh')):
          header_row = i
          break
      cols = [
          str(c).strip() if pd.notna(c) else f'Col_{i}'
          for i, c in enumerate(raw.iloc[header_row].tolist())
      ]
      df = raw.iloc[header_row + 1:].copy()
      df.columns = cols
      c_ma = find_col(df, ['Mã CH', 'Ma CH', 'Mã KH', 'Outlet_code', 'OUTLET CODE'])
      c_ct = find_col(df, ['Tên chương trình', 'Ten chuong trinh', 'Chương trình'])
      if not c_ma:
        continue
      if c_ct:
        ct = df[c_ct].astype(str).str.lower()
        mask = (
            (ct.str.contains(PROG_KEY, na=False) | ct.str.contains(PROG_KEY2, na=False))
            & (
                ct.str.contains(PROG_TEA, na=False)
                | ct.str.contains(PROG_TEA2, na=False)
                | ct.str.contains(PROG_TEA3, na=False)
            )
        )
        # fallback: MSC_BEV + Tích
        mask = mask | ct.str.contains('msc_bev', na=False) & (
            ct.str.contains('tích', na=False) | ct.str.contains('tich', na=False)
        )
        df = df[mask]
      out = set()
      for v in df[c_ma].tolist():
        if pd.isna(v):
          continue
        s = str(v).strip()
        if s.endswith('.0'):
          s = s[:-2]
        try:
          s = str(int(float(s)))
        except Exception:
          pass
        if s and s.lower() not in ('nan', 'none', ''):
          out.add(s)
      if out:
        return out
    except Exception:
      continue
  return set()


def _norm_out(x):
  if pd.isna(x):
    return ''
  s = str(x).strip()
  if s.endswith('.0'):
    s = s[:-2]
  try:
    return str(int(float(s)))
  except Exception:
    return s


def _is_tea_brand(brand, sku=''):
  t = f'{brand} {sku}'.lower()
  return any(
      k in t
      for k in (
          'bupnon', 'búp non', 'bup non', 'tea365', 'tea 365',
          'trà búp', 'tra bup',
      )
  )


def build_tea_battle_report(df_raw, df_rpt, df_mcp, report_date, filter_nv=None):
  empty_cols = [
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'L1', 'VIP', 'Thứ VT',
      'RR BEV [Triệu]', 'RR TEA [Thùng]', 'MTD BEV [Triệu]', 'MTD TEA [Thùng]',
      'SỐ SUẤT', 'GAP [Thùng]', 'ĐK D&L',
  ]
  if df_raw is None or df_raw.empty:
    return pd.DataFrame(columns=empty_cols)

  d = df_raw.copy()
  # Chuẩn hoá tên cột (hỗ trợ RAW cũ + data.xlsx mới)
  def _find_raw_col(cands):
    cols_l = {str(c).strip().lower().replace(' ', '_'): c for c in d.columns}
    # cũng match bỏ dấu _ thừa / trailing space
    cols_norm = {}
    for c in d.columns:
      k = str(c).strip().lower().replace(' ', '_').rstrip('_')
      cols_norm[k] = c
    for cand in cands:
      k = cand.strip().lower().replace(' ', '_').rstrip('_')
      if k in cols_norm:
        return cols_norm[k]
    for c in d.columns:
      cl = str(c).strip().lower()
      for cand in cands:
        if cand.lower() in cl:
          return c
    return None

  c_ma = _find_raw_col(['OUTLET_CODE', 'OUTLET CODE', 'Mã CH', 'Outlet Code'])
  c_ten = _find_raw_col(['OUTLET NAME', 'OUTLET_NAME', 'Tên CH'])
  c_nv = _find_raw_col(['SM_NAME', 'SM NAME', 'Tên NVBH'])
  c_order = _find_raw_col(['ORDER_DT', 'ORDER DATE', 'ORDER_DATE'])
  c_brand = _find_raw_col(['BRAND_DESC', 'BRAND', 'Brand'])
  c_sku = _find_raw_col([
      'STANDARD_SKU_DESC', 'ITEM_DESC', 'SKU DESC', 'SKU_DESC', 'DMS OBJ',
  ])
  c_sales = _find_raw_col(['Sales Before Discount', 'SALES_BEFORE_DISCOUNT'])
  c_cases = _find_raw_col([
      'Total Sales Cases',
      'Total Cases (Sales & Promo)',
      'TOTAL CASES',
      'Total Cases',
  ])
  c_l1 = _find_raw_col([
      'x_msc_business_type_l1', 'L1', 'Channel',
  ])
  c_month = _find_raw_col(['Month', 'MONTH'])

  d['_ma'] = d[c_ma].map(_norm_out) if c_ma else ''
  d['_ten'] = d[c_ten].astype(str).str.strip() if c_ten else ''
  d['_nv'] = d[c_nv].astype(str).str.strip() if c_nv else ''
  d['_brand'] = d[c_brand].astype(str) if c_brand else ''
  d['_sku'] = d[c_sku].astype(str) if c_sku else ''
  d['_sales'] = (
      pd.to_numeric(d[c_sales], errors='coerce').fillna(0) if c_sales else 0
  )
  d['_cases'] = (
      pd.to_numeric(d[c_cases], errors='coerce').fillna(0) if c_cases else 0
  )
  if c_order:
    d['_dt'] = pd.to_datetime(d[c_order], errors='coerce')
  elif c_month:
    # Month dạng 07/2026
    d['_dt'] = pd.to_datetime(d[c_month].astype(str), format='%m/%Y', errors='coerce')
  else:
    d['_dt'] = pd.NaT
  d['_ym'] = d['_dt'].dt.to_period('M')
  d['_tea'] = [
      _is_tea_brand(b, s) for b, s in zip(d['_brand'].tolist(), d['_sku'].tolist())
  ]
  # L1 từ raw nếu có
  if c_l1:
    d['_l1_raw'] = d[c_l1].astype(str).str.strip()
  else:
    d['_l1_raw'] = ''

  vip_map, l1_map, thu_map, ten_mcp, nv_mcp = {}, {}, {}, {}, {}
  if df_mcp is not None and not df_mcp.empty:
    c_ma = find_col(df_mcp, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    c_vip = find_col(df_mcp, ['VIP MCH', 'VIP_MCH'])
    c_l1 = find_col(df_mcp, ['L1', 'Channel'])
    c_thu = find_col(df_mcp, ['Thứ', 'Thu', 'Day'])
    c_ten = find_col(df_mcp, ['Outlet_name', 'Outlet Name', 'Tên CH', 'Tên cửa hàng'])
    c_nv = find_col(df_mcp, ['Tên NVBH', 'SM name', 'SM_NAME', 'Salesman'])
    if c_ma:
      for _, r in df_mcp.iterrows():
        ma = _norm_out(r[c_ma])
        if not ma:
          continue
        if c_vip and pd.notna(r.get(c_vip)):
          vip_map[ma] = str(r[c_vip]).strip()
        if c_l1 and pd.notna(r.get(c_l1)):
          l1_map[ma] = str(r[c_l1]).strip()
        if c_thu and pd.notna(r.get(c_thu)):
          thu_map[ma] = str(r[c_thu]).strip()
        if c_ten and pd.notna(r.get(c_ten)):
          ten_mcp[ma] = str(r[c_ten]).strip()
        if c_nv and pd.notna(r.get(c_nv)):
          nv_mcp[ma] = str(r[c_nv]).strip()

  rr_bev, rr_tea, meta = {}, {}, {}
  for ma, g in d.groupby('_ma'):
    if not ma:
      continue
    months = g['_ym'].dropna().unique()
    nm = max(len(months), 1)
    bev_sum = float(g['_sales'].sum()) / 1_000_000.0
    tea_sum = float(g.loc[g['_tea'], '_cases'].sum())
    rr_bev[ma] = round(bev_sum / nm, 2)
    rr_tea[ma] = round(tea_sum / nm, 2)
    last = g.sort_values('_dt').iloc[-1]
    meta[ma] = {
        'nv': str(last['_nv']),
        'ten': str(last['_ten']),
        'l1': str(last['_l1_raw']) if pd.notna(last.get('_l1_raw')) else '',
    }

  mtd_bev, mtd_tea = {}, {}
  if df_rpt is not None and not df_rpt.empty and 'date' in df_rpt.columns:
    rd = report_date.date() if hasattr(report_date, 'date') else report_date
    ym = (rd.year, rd.month)
    dr = df_rpt.copy()
    dr = dr[dr['date'].apply(
        lambda x: hasattr(x, 'year') and (x.year, x.month) == ym if pd.notna(x) else False
    )]
    if not dr.empty:
      dr['_ma'] = dr['Mã CH'].map(_norm_out) if 'Mã CH' in dr.columns else ''
      val_col = find_col(dr, ['Thành tiền trước CK', 'Thành tiền trước chiết khấu', 'Sales Before Discount'])
      dr['_sales'] = pd.to_numeric(dr[val_col], errors='coerce').fillna(0) if val_col else 0
      case_col = find_col(dr, ['Tổng chẵn', 'TOTAL CASES', 'Total Cases', 'Tổng Chẵn'])
      if case_col:
        dr['_cases'] = pd.to_numeric(dr[case_col], errors='coerce').fillna(0)
      else:
        sl = find_col(dr, ['Tổng lẻ', 'TOTAL PIECES', 'SL lẻ'])
        pack = find_col(dr, ['Hệ số quy đổi chẵn/lẻ', 'CASE/PACK'])
        if sl and pack:
          dr['_cases'] = (
              pd.to_numeric(dr[sl], errors='coerce').fillna(0)
              / pd.to_numeric(dr[pack], errors='coerce').replace(0, 1).fillna(1)
          )
        else:
          dr['_cases'] = 0
      if 'Tên SP lower' not in dr.columns:
        sp = dr['Tên sản phẩm'] if 'Tên sản phẩm' in dr.columns else ''
        dr['Tên SP lower'] = pd.Series(sp, index=dr.index).astype(str).str.lower()
      dr['_tea'] = dr['Tên SP lower'].map(lambda t: _is_tea_brand('', t))
      bev_kw = (
          r'wake up|wakeup|247|tea365|búp non|bupnon|vivant|lemona|vĩnh hảo|'
          r'vinh hao|nước|nuoc|trà|tra |café|coffee'
      )
      dr['_bev'] = dr['Tên SP lower'].str.contains(bev_kw, case=False, na=False, regex=True)
      for ma, g in dr.groupby('_ma'):
        if not ma:
          continue
        mtd_bev[ma] = round(float(g.loc[g['_bev'], '_sales'].sum()) / 1_000_000.0, 2)
        mtd_tea[ma] = round(float(g.loc[g['_tea'], '_cases'].sum()), 2)

  dk_set = load_dk_tea_outlets()
  all_ma = sorted(set(rr_bev.keys()) | set(mtd_tea.keys()) | set(mtd_bev.keys()))
  rows = []
  for ma in all_ma:
    if not ma:
      continue
    m = meta.get(ma, {})
    nv = nv_mcp.get(ma) or m.get('nv', '')
    ten = ten_mcp.get(ma) or m.get('ten', '')
    l1 = l1_map.get(ma) or m.get('l1', '')
    vip = vip_map.get(ma, '')
    thu = thu_map.get(ma, '')
    rb = rr_bev.get(ma, 0.0)
    rt = rr_tea.get(ma, 0.0)
    mb = mtd_bev.get(ma, 0.0)
    mt = mtd_tea.get(ma, 0.0)
    if mt >= 20:
      suat = 2
    elif mt >= 10:
      suat = 1
    else:
      suat = 0
    gap = round(max(0.0, 10.0 - mt), 2) if mt < 10 else 0.0
    dk = '✓' if ma in dk_set else ''
    rows.append({
        'Tên NVBH': nv,
        'Mã KH': ma,
        'Tên KH': ten,
        'L1': l1,
        'VIP': vip,
        'Thứ VT': thu,
        'RR BEV [Triệu]': rb,
        'RR TEA [Thùng]': rt,
        'MTD BEV [Triệu]': mb,
        'MTD TEA [Thùng]': mt,
        'SỐ SUẤT': suat,
        'GAP [Thùng]': gap,
        'ĐK D&L': dk,
    })

  out = pd.DataFrame(rows)
  if out.empty:
    return pd.DataFrame(columns=empty_cols)
  # Chỉ hiển thị CH có RR BEV >= 3 triệu
  if 'RR BEV [Triệu]' in out.columns:
    out = out[pd.to_numeric(out['RR BEV [Triệu]'], errors='coerce').fillna(0) >= 3.0]
  if out.empty:
    return pd.DataFrame(columns=empty_cols)
  if filter_nv:
    vals = [
        str(v).strip()
        for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])
        if str(v).strip()
    ]
    if vals:
      out = out[out['Tên NVBH'].isin(vals)]
  out = out.sort_values(['Tên NVBH', 'Mã KH']).reset_index(drop=True)
  out.insert(0, 'STT', range(1, len(out) + 1))
  return out


def render_tea_battle_html(df):
  if df is None or df.empty:
    return '<p style="color:#718096;">Không có dữ liệu chi tiết cửa hàng.</p>'
  cols = [
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'L1', 'VIP', 'Thứ VT',
      'RR BEV [Triệu]', 'RR TEA [Thùng]', 'MTD BEV [Triệu]', 'MTD TEA [Thùng]',
      'SỐ SUẤT', 'GAP [Thùng]', 'ĐK D&L',
  ]
  for c in cols:
    if c not in df.columns:
      df[c] = ''

  max_name = 12
  for n in df['Tên NVBH'].astype(str):
    max_name = max(max_name, len(n))
  name_w = max(150, min(260, max_name * 9 + 24))
  stt_w = 48
  sh_stt = 'box-shadow:2px 0 0 0 #2b6cb0;'
  sh_ten = 'box-shadow:4px 0 6px -2px rgba(0,0,0,.25);'

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 5px;font-size:11px;'
      'white-space:nowrap;'
  )
  td = (
      'border:1px solid #bce2f5 !important;padding:5px 4px;font-size:11px;'
      'white-space:nowrap;'
  )
  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:8px;">',
      '<h4 style="color:#1a365d;font-weight:800;margin:8px 0 6px 0;">'
      '📋 CHI TIẾT TỪNG KH THEO NHÂN VIÊN</h4>',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;'
      'width:max-content;min-width:100%;font-family:Arial,sans-serif;"><thead><tr>',
  ]
  for c in cols:
    if c == 'STT':
      html.append(
          f'<th style="{th}position:sticky;left:0;z-index:8;'
          f'min-width:{stt_w}px;max-width:{stt_w}px;{sh_stt}">STT</th>'
      )
    elif c == 'Tên NVBH':
      html.append(
          f'<th style="{th}position:sticky;left:{stt_w}px;z-index:8;'
          f'min-width:{name_w}px;max-width:{name_w}px;text-align:left !important;{sh_ten}">'
          f'Tên NVBH</th>'
      )
    else:
      html.append(f'<th style="{th}">{c}</th>')
  html.append('</tr></thead><tbody>')
  for pos, (_, row) in enumerate(df.iterrows()):
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr>')
    for c in cols:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      al = 'left' if c in ('Tên NVBH', 'Tên KH', 'L1') else 'center'
      if c == 'STT':
        base = (
            f'{td}position:sticky;left:0;z-index:5;min-width:{stt_w}px;max-width:{stt_w}px;'
            f'background-color:{bg} !important;text-align:center !important;{sh_stt}'
        )
      elif c == 'Tên NVBH':
        base = (
            f'{td}position:sticky;left:{stt_w}px;z-index:5;min-width:{name_w}px;max-width:{name_w}px;'
            f'background-color:{bg} !important;text-align:left !important;font-weight:600;{sh_ten}'
        )
      else:
        base = (
            f'{td}background-color:{bg} !important;text-align:{al} !important;'
        )
      if c == 'SỐ SUẤT':
        try:
          s = int(float(str(val).replace('(RỚT)', '').strip() or 0))
        except Exception:
          s = 0
        if s <= 0:
          html.append(
              f'<td data-colored="1" class="suat-rot" style="{base}">0 (RỚT)</td>'
          )
        else:
          html.append(
              f'<td data-colored="1" class="suat-ok" style="{base}">{s}</td>'
          )
        continue
      if c == 'ĐK D&L' and str(val).strip() in ('✓', '✔'):
        html.append(
            f'<td style="{base}color:#228b22 !important;font-weight:900 !important;">{val}</td>'
        )
        continue
      html.append(f'<td style="{base}">{val}</td>')
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def _resolve_perf_sku_path():
  names = [
      'TARGETACTUAL BY STD SKU -BY SM.xlsx',
      'TARGETACTUAL BY STD SKU -BY SM.xls',
      'TARGETACTUAL_BY_STD_SKU_BY_SM.xlsx',
  ]
  for n in names:
    p = os.path.join(get_data_dir(), n)
    if os.path.isfile(p):
      return p
  if os.path.isdir(get_data_dir()):
    for fn in os.listdir(get_data_dir()):
      low = fn.lower().replace(' ', '').replace('_', '').replace('-', '')
      if fn.lower().endswith(('.xlsx', '.xls')) and 'targetactual' in low and 'sku' in low:
        return os.path.join(get_data_dir(), fn)
  return os.path.join(get_data_dir(), 'TARGETACTUAL BY STD SKU -BY SM.xlsx')


@st.cache_data(ttl=600)
def load_perf_sku_data():
  path = _resolve_perf_sku_path()
  if not os.path.isfile(path):
    return pd.DataFrame()
  try:
    raw = pd.read_excel(path, header=None, dtype=object)
    header_row = 0
    for i in range(min(10, len(raw))):
      vals = [str(x).strip().lower() for x in raw.iloc[i].tolist() if pd.notna(x)]
      joined = ' | '.join(vals)
      if 'month' in joined and ('sm name' in joined or 'target' in joined or 'sub div' in joined):
        header_row = i
        break
    cols = []
    for _i, _c in enumerate(raw.iloc[header_row].tolist()):
      if pd.isna(_c):
        cols.append(f'Col_{_i}')
      else:
        _name = str(_c).strip()
        if len(_name) >= 2 and _name[0] in chr(34)+chr(39) and _name[-1] == _name[0]:
          _name = _name[1:-1].strip()
        cols.append(_name)
    df = raw.iloc[header_row + 1:].copy()
    df.columns = cols
    return df
  except Exception:
    return pd.DataFrame()




def _month_key_from_date(d):
  """date/datetime → 'MM/YYYY'."""
  try:
    if hasattr(d, 'month'):
      return f'{int(d.month):02d}/{int(d.year)}'
  except Exception:
    pass
  return ''


def build_rpt_sellout_maps(df_rpt, report_date):
  """SellOut tháng T từ RPT — cùng rule TURNOVER.

  - Cột tiền: **Thành tiền trước CK** (không dùng Tổng tiền / sau CK)
  - Chỉ loại đơn **Đã hủy** (giống load_main_data; không loại pending)
  - Kỳ: từ đầu tháng → hết tháng của report_date
  """
  by_cat, by_nv_cat = {}, {}
  if df_rpt is None or getattr(df_rpt, 'empty', True) or report_date is None:
    return by_cat, by_nv_cat
  d = df_rpt.copy()
  # Ưu tiên cột date đã chuẩn hoá từ load_main_data
  if 'date' in d.columns:
    d['_d'] = pd.to_datetime(d['date'], errors='coerce')
  else:
    c_date = find_col(d, [
        'Ngày tạo đơn hàng', 'Ngày tạo đơn', 'Order Date', 'ORDER_DT',
    ])
    if not c_date:
      return by_cat, by_nv_cat
    d['_d'] = pd.to_datetime(d[c_date], dayfirst=True, errors='coerce')

  c_cat = find_col(d, ['Sub Division', 'SUB DIV', 'SubDivision', 'Phân nhóm'])
  c_nv = find_col(d, ['Tên NVBH', 'SM NAME', 'SM_NAME', 'Nhân viên'])
  # Cùng TURNOVER: Thành tiền trước CK
  c_val = find_col(d, [
      'Thành tiền trước CK', 'Thành tiền trước chiết khấu',
      'Tổng tiền', 'Giá trị sau CK', 'Doanh thu',
  ])
  c_status = find_col(d, ['Tình trạng đơn hàng', 'Status', 'STATUS_CD'])
  if not c_cat or not c_val:
    return by_cat, by_nv_cat

  y, m = int(report_date.year), int(report_date.month)
  d = d[d['_d'].apply(
      lambda x: (int(x.year), int(x.month)) == (y, m) if pd.notna(x) else False
  )]
  # Chỉ loại Đã hủy — khớp load_main_data / TURNOVER
  if c_status:
    st = d[c_status].astype(str).str.strip().str.lower()
    d = d[~st.isin(['đã hủy', 'da huy', 'cancelled', 'canceled'])]
    d = d[~st.str.contains('hủy|huy', na=False)]

  d['_cat'] = d[c_cat].astype(str).str.strip()
  d['_val'] = pd.to_numeric(d[c_val], errors='coerce').fillna(0)
  if c_nv:
    d['_nv'] = d[c_nv].astype(str).str.strip()
  else:
    d['_nv'] = ''
  by_cat = d.groupby('_cat')['_val'].sum().to_dict()
  by_nv_cat = d.groupby(['_nv', '_cat'])['_val'].sum().to_dict()
  return by_cat, by_nv_cat

def build_perf_by_month(df_raw, filter_nv=None, n_months=4, df_rpt=None, report_date=None):
  """4 tháng gần nhất: bảng CAT / Target / SellOut / %MTD.

  Tháng T (tháng report_date): SellOut lấy từ RPT (DanhSachChiTietDonHang).
  Các tháng trước: SellOut lấy từ file TARGETACTUAL (cột SO).
  """
  empty = pd.DataFrame(columns=['CAT', 'Target', 'SellOut', '%MTD'])
  if df_raw is None or df_raw.empty:
    return {}, []
  d = df_raw.copy()
  c_month = find_col(d, ['MONTH', 'Month'])
  c_cat = find_col(d, ['SUB DIV', 'SUB_DIV', 'CAT', 'Category'])
  c_so = find_col(d, ['SO', 'SellOut', 'Sell Out'])
  c_tg = find_col(d, ['TARGET SO', 'Target SO', 'TARGET', 'Target'])
  c_nv = find_col(d, ['SM NAME', 'SM_NAME', 'Tên NVBH'])
  if not c_month or not c_cat:
    return {}, []
  d['_month'] = d[c_month].astype(str).str.strip()
  d['_cat'] = d[c_cat].astype(str).str.strip()
  d['_cat'] = d['_cat'].replace({'': '(blank)', 'nan': '(blank)', 'None': '(blank)'})
  d['_so'] = pd.to_numeric(d[c_so], errors='coerce').fillna(0) if c_so else 0
  d['_tg'] = pd.to_numeric(d[c_tg], errors='coerce').fillna(0) if c_tg else 0
  if filter_nv and c_nv:
    d = d[d[c_nv].astype(str).isin([str(x) for x in filter_nv])]
  # Parse month key for sort: MM/YYYY
  def _mk(m):
    try:
      parts = str(m).split('/')
      return (int(parts[1]), int(parts[0]))
    except Exception:
      return (0, 0)
  months = sorted(d['_month'].dropna().unique().tolist(), key=_mk, reverse=True)
  months = months[:n_months]
  # RPT sellout tháng T
  cur_m = _month_key_from_date(report_date) if report_date is not None else ''
  rpt_by_cat, _ = build_rpt_sellout_maps(df_rpt, report_date)

  result = {}
  for m in months:
    g = d[d['_month'] == m].groupby('_cat', as_index=False).agg(
        Target=('_tg', 'sum'), SellOut=('_so', 'sum')
    )
    g = g.rename(columns={'_cat': 'CAT'})
    # Tháng hiện tại → SellOut từ RPT
    if m == cur_m and rpt_by_cat:
      g['SellOut'] = g['CAT'].map(
          lambda c: float(rpt_by_cat.get(str(c), 0) or 0)
      )
      # Thêm CAT có trên RPT nhưng chưa có target row
      existing = set(g['CAT'].astype(str))
      extra = []
      for cat, amt in rpt_by_cat.items():
        if cat not in existing and float(amt or 0) > 0:
          extra.append({'CAT': cat, 'Target': 0.0, 'SellOut': float(amt)})
      if extra:
        g = pd.concat([g, pd.DataFrame(extra)], ignore_index=True)
    g['%MTD'] = g.apply(
        lambda r: round(float(r['SellOut']) / float(r['Target']) * 100, 0)
        if float(r['Target'] or 0) > 0
        else 0.0,
        axis=1,
    )
    # sort by Target desc, blank last
    g['_ord'] = g['CAT'].apply(lambda x: 1 if str(x).lower() in ('(blank)', 'blank', 'nan') else 0)
    g = g.sort_values(['_ord', 'Target'], ascending=[True, False]).drop(columns=['_ord'])
    # Căn Target ngành theo tổng Target Turnover (đúng như TURNOVER)
    try:
      _to_by_name = get_turnover_targets_by_name()
      if _to_by_name:
        if filter_nv:
          names = [str(x).strip() for x in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
          to_total = 0.0
          for nm in names:
            to_total += float(_to_by_name.get(nm) or _to_by_name.get(nm.lower()) or 0)
        else:
          # team: sum unique names (skip .lower duplicates)
          seen = set()
          to_total = 0.0
          for k, v in _to_by_name.items():
            if k != k.lower() or k.lower() not in seen:
              if k == k.lower() and any(k == x.lower() and x != k for x in _to_by_name):
                continue
              to_total += float(v or 0)
              seen.add(k.lower())
        sku_total = float(g['Target'].sum())
        if to_total > 0 and sku_total > 0:
          # Cả hai nguồn đều VND
          _ratio = float(to_total) / float(sku_total)
          if 0.5 <= _ratio <= 3.0:
            g['Target'] = g['Target'].astype(float) * _ratio
            g['%MTD'] = g.apply(
                lambda r: round(float(r['SellOut']) / float(r['Target']) * 100, 0)
                if float(r['Target'] or 0) > 0 else 0.0,
                axis=1,
            )
    except Exception:
      pass
    # Grand Total
    tot_t = float(g['Target'].sum())
    tot_s = float(g['SellOut'].sum())
    tot = pd.DataFrame([{
        'CAT': 'Grand Total',
        'Target': tot_t,
        'SellOut': tot_s,
        '%MTD': round(tot_s / tot_t * 100, 0) if tot_t > 0 else 0.0,
    }])
    g = pd.concat([g, tot], ignore_index=True)
    result[m] = g
  return result, months


def _fmt_perf_num(v, div_million=True):
  """Hiển thị số (mặc định ÷ 1.000.000 — đơn vị triệu)."""
  try:
    n = float(v)
    if div_million:
      n = n / 1_000_000.0
      return f'{n:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'{n:,.0f}'.replace(',', '.')
  except Exception:
    return str(v) if v is not None else ''


def render_perf_table_html(df, month_label, use_timegone=False):
  if df is None or df.empty:
    return ''
  cols = ['CAT', 'Target', 'SellOut', '%MTD']
  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:7px 8px;font-size:12px;'
  )
  td = (
      'border:1px solid #bce2f5 !important;padding:5px 8px;font-size:12px;'
  )
  tot_s = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;border:1px solid #2b6cb0 !important;'
      'padding:5px 8px;font-size:12px;'
  )
  html = [
      f'<h4 style="color:#1a365d;font-weight:800;margin:12px 0 6px 0;">'
      f'📅 Tháng {month_label}</h4>',
      '<div style="overflow-x:auto;margin-bottom:8px;">',
      '<table class="custom-kpi-table" style="border-collapse:collapse;width:100%;'
      'max-width:560px;font-family:Arial,sans-serif;"><thead><tr>',
  ]
  for c in cols:
    html.append(f'<th style="{th}">{c}</th>')
  html.append('</tr></thead><tbody>')
  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = str(row.get('CAT', '')).strip().lower() in ('grand total', 'tổng cộng', 'total')
    bg = '#1a365d' if is_tot else ('#e6f4fc' if pos % 2 == 0 else '#ffffff')
    fg = '#ffffff' if is_tot else '#1a202c'
    html.append('<tr class="row-total">' if is_tot else '<tr>')
    for c in cols:
      val = row.get(c, '')
      if c in ('Target', 'SellOut'):
        disp = _fmt_perf_num(val)
      elif c == '%MTD':
        try:
          disp = f'{int(float(val))}%'
        except Exception:
          disp = str(val)
      else:
        disp = val
      al = 'left' if c == 'CAT' else 'right' if c in ('Target', 'SellOut') else 'center'
      if is_tot:
        html.append(
            f'<td class="row-total-cell" style="{tot_s}text-align:{al} !important;">{disp}</td>'
        )
      elif c == '%MTD':
        if use_timegone:
          try:
            _moc = float(_CURRENT_TIMEGONE)
          except Exception:
            _moc = 100.0
        else:
          _moc = 100.0
        cls = color_pct_class(val, moc=_moc)
        bg = color_pct_bg(val, moc=_moc)
        html.append(
            f'<td data-colored="1" class="{cls}" style="{bg}text-align:center !important;'
            f'border:1px solid #bce2f5 !important;padding:5px 8px;font-size:12px;'
            f'font-weight:700 !important;">{disp}</td>'
        )
      else:
        html.append(
            f'<td style="{td}background-color:{bg} !important;color:{fg} !important;'
            f'text-align:{al} !important;">{disp}</td>'
        )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)


def render_perf_chart(df, month_label):
  """Horizontal grouped bar: TARGET (cam) + SO (xanh) — không chồng lấn."""
  if df is None or df.empty:
    return
  d = df[~df['CAT'].astype(str).str.lower().isin(
      ['grand total', 'tổng cộng', 'total']
  )].copy()
  if d.empty:
    return

  d = d.copy()
  d['SellOut'] = pd.to_numeric(d['SellOut'], errors='coerce').fillna(0) / 1_000_000.0
  d['Target'] = pd.to_numeric(d['Target'], errors='coerce').fillna(0) / 1_000_000.0
  cats = [str(c) for c in d['CAT'].tolist()]
  # Đảo thứ tự để CAT đầu hiện trên cùng (giống mẫu)
  cats_plot = list(reversed(cats))
  so_vals = [float(d.loc[d['CAT'].astype(str) == c, 'SellOut'].iloc[0]) if len(d.loc[d['CAT'].astype(str) == c]) else 0.0 for c in cats_plot]
  tg_vals = [float(d.loc[d['CAT'].astype(str) == c, 'Target'].iloc[0]) if len(d.loc[d['CAT'].astype(str) == c]) else 0.0 for c in cats_plot]

  try:
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=cats_plot,
        x=tg_vals,
        name='Sum of TARGET SO',
        orientation='h',
        marker_color='#ED7D31',
        hovertemplate='<b>%{y}</b><br>TARGET: %{x:,.1f} triệu<extra></extra>',
    ))
    fig.add_trace(go.Bar(
        y=cats_plot,
        x=so_vals,
        name='Sum of SO',
        orientation='h',
        marker_color='#4472C4',
        hovertemplate='<b>%{y}</b><br>SO: %{x:,.1f} triệu<extra></extra>',
    ))
    fig.update_layout(
        barmode='group',  # cạnh nhau, không chồng
        bargap=0.25,
        bargroupgap=0.08,
        title_text=f'📅 Tháng {month_label}',
        title_x=0.5,
        title_font_size=16,
        title_font_color='#1a365d',
        height=max(360, 36 * len(cats) + 80),
        margin=dict(l=10, r=20, t=50, b=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.18,
            xanchor='center',
            x=0.5,
            font_size=12,
        ),
        xaxis=dict(
            gridcolor='#e2e8f0',
            zeroline=False,
            tickfont=dict(size=11, color='#334155'),
        ),
        yaxis=dict(
            tickfont=dict(size=12, color='#334155'),
            automargin=True,
        ),
    )
    st.plotly_chart(fig, use_container_width=True)
    return
  except ImportError:
    pass

  # Fallback Altair nếu không có plotly
  import altair as alt
  plot = pd.DataFrame({
      'CAT': cats_plot * 2,
      'Chỉ số': ['Sum of TARGET SO'] * len(cats_plot) + ['Sum of SO'] * len(cats_plot),
      'Giá trị': tg_vals + so_vals,
  })
  chart = (
      alt.Chart(plot)
      .mark_bar()
      .encode(
          y=alt.Y('CAT:N', sort=cats_plot, title=None),
          x=alt.X('Giá trị:Q', title=None),
          color=alt.Color(
              'Chỉ số:N',
              scale=alt.Scale(
                  domain=['Sum of TARGET SO', 'Sum of SO'],
                  range=['#ED7D31', '#4472C4'],
              ),
              legend=alt.Legend(title=None, orient='bottom'),
          ),
          yOffset='Chỉ số:N',
          tooltip=['CAT:N', 'Chỉ số:N', alt.Tooltip('Giá trị:Q', format=',.1f')],
      )
      .properties(height=max(320, 28 * len(cats) + 60), title=f'📅 Tháng {month_label}')
      .configure_title(fontSize=16, fontWeight='bold', color='#1a365d', anchor='middle')
  )
  st.altair_chart(chart, use_container_width=True)



def build_perf_nv_matrix(df_raw, month, filter_nv=None, df_rpt=None, report_date=None):
  """Pivot NV × SUB DIV: TARGET / SELL OUT / % MTD. Ẩn ngành không có chỉ tiêu.

  Tháng T: SELL OUT lấy từ RPT; tháng khác lấy từ cột SO file Target.
  """
  if df_raw is None or df_raw.empty or not month:
    return pd.DataFrame(), []
  d = df_raw.copy()
  c_month = find_col(d, ['MONTH', 'Month'])
  c_cat = find_col(d, ['SUB DIV', 'SUB_DIV', 'CAT', 'Category'])
  c_so = find_col(d, ['SO', 'SellOut', 'Sell Out'])
  c_tg = find_col(d, ['TARGET SO', 'Target SO', 'TARGET', 'Target'])
  c_nv = find_col(d, ['SM NAME', 'SM_NAME', 'Tên NVBH'])
  if not all([c_month, c_cat, c_nv]):
    return pd.DataFrame(), []
  d = d[d[c_month].astype(str).str.strip() == str(month).strip()]
  if filter_nv:
    d = d[d[c_nv].astype(str).isin([str(x) for x in filter_nv])]
  d['_nv'] = d[c_nv].astype(str).str.strip()
  d['_cat'] = d[c_cat].astype(str).str.strip()
  d['_cat'] = d['_cat'].replace({'': '(blank)', 'nan': '(blank)', 'None': '(blank)'})
  d['_so'] = pd.to_numeric(d[c_so], errors='coerce').fillna(0) if c_so else 0
  d['_tg'] = pd.to_numeric(d[c_tg], errors='coerce').fillna(0) if c_tg else 0
  # Bỏ blank category — hiển thị đủ SUB DIV (kể cả không có chỉ tiêu)
  d = d[~d['_cat'].str.lower().isin(['(blank)', 'blank', 'nan', ''])]
  cat_tg = d.groupby('_cat')['_tg'].sum()
  # Sort: có target trước (desc), rồi tên
  cats = sorted(
      cat_tg.index.tolist(),
      key=lambda c: (-float(cat_tg[c] or 0), str(c)),
  )
  if not cats:
    return pd.DataFrame(), []
  g = d.groupby(['_nv', '_cat'], as_index=False).agg(tg=('_tg', 'sum'), so=('_so', 'sum'))
  # Tháng T → thay SO bằng RPT
  cur_m = _month_key_from_date(report_date) if report_date is not None else ''
  if str(month).strip() == cur_m:
    _, rpt_nv_cat = build_rpt_sellout_maps(df_rpt, report_date)
    if rpt_nv_cat:
      # rebuild so from RPT
      g['_key'] = list(zip(g['_nv'].astype(str), g['_cat'].astype(str)))
      g['so'] = g['_key'].map(lambda k: float(rpt_nv_cat.get(k, 0) or 0))
      # thêm NV/CAT có trên RPT
      extra_rows = []
      existing = set(g['_key'].tolist())
      for (nv, cat), amt in rpt_nv_cat.items():
        if (nv, cat) not in existing and float(amt or 0) > 0:
          # chỉ thêm cat đã có target team-level
          if cat in cats:
            extra_rows.append({'_nv': nv, '_cat': cat, 'tg': 0.0, 'so': float(amt)})
      if extra_rows:
        g = pd.concat([g, pd.DataFrame(extra_rows)], ignore_index=True)
  nvs = sorted(g['_nv'].dropna().unique().tolist())
  rows = []
  for nv in nvs:
    row = {'Tên NVBH': nv}
    tot_tg = 0.0
    tot_so = 0.0
    sub = g[g['_nv'] == nv]
    for cat in cats:
      r = sub[sub['_cat'] == cat]
      tg = float(r['tg'].sum()) if len(r) else 0.0
      so = float(r['so'].sum()) if len(r) else 0.0
      pct = round(so / tg * 100, 0) if tg > 0 else 0.0
      row[f'{cat}|TARGET'] = tg
      row[f'{cat}|SELL OUT'] = so
      row[f'{cat}|% MTD'] = pct
      tot_tg += tg
      tot_so += so
    row['TOTAL|TARGET'] = tot_tg
    row['TOTAL|SELL OUT'] = tot_so
    row['TOTAL|% MTD'] = round(tot_so / tot_tg * 100, 0) if tot_tg > 0 else 0.0
    rows.append(row)
  out = pd.DataFrame(rows)
  if out.empty:
    return out, cats
  # Căn TARGET theo Target Turnover (Target_KPI) — nguồn đúng như Báo Cáo TURNOVER
  try:
    _to_by_name = get_turnover_targets_by_name()
    if _to_by_name and not out.empty:
      for i, row in out.iterrows():
        nv = str(row.get('Tên NVBH', '')).strip()
        to_tgt = _to_by_name.get(nv) or _to_by_name.get(nv.lower()) or 0
        if not to_tgt or float(to_tgt) <= 0:
          continue
        # Cả Target_KPI và TARGET SO trong file đều là VND (hiển thị ÷1e6)
        scaled = _scale_row_targets_to_turnover(dict(row), cats, float(to_tgt))
        for k, v in scaled.items():
          if k in out.columns:
            out.at[i, k] = v
  except Exception:
    pass
  # Total row
  tot = {'Tên NVBH': 'TỔNG CỘNG'}
  for cat in cats:
    tot[f'{cat}|TARGET'] = float(out[f'{cat}|TARGET'].sum())
    tot[f'{cat}|SELL OUT'] = float(out[f'{cat}|SELL OUT'].sum())
    t = tot[f'{cat}|TARGET']
    s = tot[f'{cat}|SELL OUT']
    tot[f'{cat}|% MTD'] = round(s / t * 100, 0) if t > 0 else 0.0
  tot['TOTAL|TARGET'] = float(out['TOTAL|TARGET'].sum())
  tot['TOTAL|SELL OUT'] = float(out['TOTAL|SELL OUT'].sum())
  tt = tot['TOTAL|TARGET']
  ts = tot['TOTAL|SELL OUT']
  tot['TOTAL|% MTD'] = round(ts / tt * 100, 0) if tt > 0 else 0.0
  out = pd.concat([out, pd.DataFrame([tot])], ignore_index=True)
  out.insert(0, 'STT', [
      str(i + 1) if i < len(out) - 1 else '' for i in range(len(out))
  ])
  return out, cats



def render_perf_subdiv_charts(df_mat, cats):
  """8 chart SUB DIV — modebar fullsize từng chart + Ẩn/Hiện + màu tên NV."""
  if df_mat is None or df_mat.empty or not cats:
    return

  d = df_mat.copy()
  if 'Tên NVBH' not in d.columns:
    return
  mask_tot = d['Tên NVBH'].astype(str).str.upper().str.contains(
      'TỔNG|TOTAL|SS ', na=False
  )
  d = d[~mask_tot].copy()
  if d.empty:
    return

  nvs = [str(x) for x in d['Tên NVBH'].tolist()]
  cats_show = [c for c in cats if c][:8]
  while len(cats_show) < 8:
    cats_show.append(None)

  try:
    import plotly.graph_objects as go
  except ImportError:
    st.caption('Cần plotly để xem chart SUB DIV.')
    return

  try:
    moc = float(_CURRENT_TIMEGONE)
  except Exception:
    moc = 100.0

  # Tiêu đề + nút Ẩn/Hiện ngay sau
  st.markdown(
      '<h4 style="color:#1a365d;font-weight:800;margin:16px 0 2px 0;">'
      '📊 CHART THEO TỪNG NGÀNH HÀNG (SUB DIV)</h4>',
      unsafe_allow_html=True,
  )
  show_charts = st.toggle(
      '👁️ Hiện / Ẩn toàn bộ Chart',
      value=True,
      key='perf_subdiv_show_hide',
  )
  if not show_charts:
    st.caption('Chart đang ẩn — bật toggle phía trên để hiện lại.')
    return

  st.markdown(
      '<p style="font-size:12px;color:#64748b;margin:4px 0 8px 0;">'
      '🟠 TARGET &nbsp;|&nbsp; 🔵 SO'
      ' &nbsp;·&nbsp; Tên <b style="color:#c53030;">đỏ đậm</b> = dưới Timegone'
      ' &nbsp;·&nbsp; Tên <b style="color:#0b1f4a;">xanh dương đậm</b> = kịp / vượt'
      f' ({moc:.0f}%)'
      ' &nbsp;·&nbsp; Bấm icon <b>⛶</b> trên từng chart để xem fullsize</p>',
      unsafe_allow_html=True,
  )

  def _build_fig(cat):
    col_tg = f'{cat}|TARGET'
    col_so = f'{cat}|SELL OUT'
    tg, so, pcts = [], [], []
    for _, r in d.iterrows():
      try:
        v_tg = float(r.get(col_tg, 0) or 0) / 1_000_000.0
      except Exception:
        v_tg = 0.0
      try:
        v_so = float(r.get(col_so, 0) or 0) / 1_000_000.0
      except Exception:
        v_so = 0.0
      tg.append(v_tg)
      so.append(v_so)
      pcts.append(round(v_so / v_tg * 100, 1) if v_tg > 0 else 0.0)

    nvs_p = list(reversed(nvs))
    tg_p = list(reversed(tg))
    so_p = list(reversed(so))
    pct_p = list(reversed(pcts))

    ticktext = []
    for i, name in enumerate(nvs_p):
      if pct_p[i] < moc:
        ticktext.append(
            f'<span style="color:#c53030;font-weight:700">{name}</span>'
        )
      else:
        # Kịp / vượt Timegone → xanh dương đậm
        ticktext.append(
            f'<span style="color:#0b1f4a;font-weight:700">{name}</span>'
        )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=nvs_p, x=tg_p, name='TARGET', orientation='h',
        marker_color='#ED7D31',
        hovertemplate='<b>%{y}</b><br>TARGET: %{x:,.1f} tr'
                      '<br>%: %{customdata:.1f}%<extra></extra>',
        customdata=pct_p,
    ))
    fig.add_trace(go.Bar(
        y=nvs_p, x=so_p, name='SO', orientation='h',
        marker_color='#4472C4',
        hovertemplate='<b>%{y}</b><br>SO: %{x:,.1f} tr<extra></extra>',
    ))
    fig.update_layout(
        barmode='group',
        bargap=0.2,
        bargroupgap=0.05,
        title=dict(
            text=f'<b>{cat}</b>',
            font=dict(size=13, color='#1a365d'),
            x=0.5, xanchor='center', y=0.98, yanchor='top',
        ),
        height=max(280, 24 * len(nvs) + 50),
        margin=dict(l=4, r=8, t=40, b=8),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            gridcolor='#e2e8f0', zeroline=False,
            tickfont=dict(size=9),
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=nvs_p,
            ticktext=ticktext,
            tickfont=dict(size=10),
            automargin=True,
        ),
    )
    return fig

  # Modebar chỉ hiện khi hover/click — giống chart tháng bên dưới
  plot_cfg = {
      'displayModeBar': 'hover',
      'displaylogo': False,
      'modeBarButtonsToRemove': [
          'select2d', 'lasso2d', 'autoScale2d',
          'hoverClosestCartesian', 'hoverCompareCartesian',
      ],
      'toImageButtonOptions': {
          'format': 'png',
          'filename': 'perf_subdiv',
      },
  }

  for row_i in range(2):
    cols = st.columns(4)
    for col_i in range(4):
      cat = cats_show[row_i * 4 + col_i]
      with cols[col_i]:
        if not cat:
          st.empty()
          continue
        try:
          box = st.container(border=True)
        except TypeError:
          box = st.container()
        with box:
          st.plotly_chart(
              _build_fig(cat),
              use_container_width=True,
              config=plot_cfg,
          )



def render_perf_nv_matrix_html(df, cats, month_label, use_timegone=True):
  """Bảng tổng hợp NV × ngành — sticky STT/Tên NVBH + header, cuộn ngang như Trưng bày."""
  if df is None or df.empty or not cats:
    return ''

  name_w = 150
  # Ước lượng độ rộng cột tên theo tên dài nhất
  try:
    max_len = int(df['Tên NVBH'].astype(str).str.len().max())
    name_w = max(140, min(220, max_len * 8 + 20))
  except Exception:
    pass

  th = (
      'background-color:#ffd700 !important;color:#1a202c !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #d69e2e !important;padding:5px 4px;font-size:10px;'
      'white-space:nowrap;'
  )
  th_sub = (
      'background-color:#ffe066 !important;color:#1a202c !important;'
      'font-weight:700 !important;text-align:center !important;'
      'border:1px solid #d69e2e !important;padding:3px 3px;font-size:9px;'
      'white-space:nowrap;'
  )
  sticky_stt_h = (
      f'{th}position:sticky;left:0;z-index:6;min-width:44px;max-width:44px;'
  )
  sticky_ten_h = (
      f'{th}position:sticky;left:44px;z-index:6;min-width:{name_w}px;'
  )
  sticky_stt_c = (
      'position:sticky;left:0;z-index:2;min-width:44px;max-width:44px;'
  )
  sticky_ten_c = (
      f'position:sticky;left:44px;z-index:2;min-width:{name_w}px;'
  )
  td = (
      'border:1px solid #e2e8f0 !important;padding:3px 4px;font-size:10px;'
      'text-align:center !important;white-space:nowrap;'
  )
  tot_s = (
      'background-color:#ffd700 !important;color:#1a202c !important;'
      'font-weight:900 !important;border:1px solid #d69e2e !important;'
      'padding:3px 4px;font-size:10px;'
  )
  n_metric = 3

  html = [
      f'<h4 style="color:#1a365d;font-weight:800;margin:8px 0 4px 0;">'
      f'📊 TỔNG HỢP PERFORMANCE THEO NHÂN VIÊN — {month_label}'
      f' <span style="font-size:12px;font-weight:600;color:#718096;">'
      f'(đơn vị: triệu đồng)</span></h4>',
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:14px;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;'
      'width:max-content;min-width:100%;font-family:Arial,sans-serif;">',
      '<thead style="position:sticky;top:0;z-index:5;">',
      '<tr>',
      f'<th rowspan="2" style="{sticky_stt_h}">STT</th>',
      f'<th rowspan="2" style="{sticky_ten_h}">TÊN NVBH</th>',
  ]
  for cat in cats:
    html.append(f'<th colspan="{n_metric}" style="{th}">{cat}</th>')
  html.append(f'<th colspan="{n_metric}" style="{th}">TARGET</th>')
  html.append('</tr><tr>')
  for _ in list(cats) + ['TOTAL']:
    for sub in ('TARGET', 'SELL OUT', '% MTD'):
      html.append(f'<th style="{th_sub}">{sub}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    bg = '#ffd700' if is_tot else ('#fffff0' if pos % 2 == 0 else '#ffffff')
    fg = '#1a202c'
    html.append('<tr class="row-total">' if is_tot else '<tr>')

    # STT sticky
    stt_val = row.get('STT', '')
    if pd.isna(stt_val):
      stt_val = ''
    html.append(
        f'<td style="{sticky_stt_c}{td}background-color:{bg} !important;'
        f'color:{fg} !important;font-weight:{"900" if is_tot else "600"} !important;">'
        f'{stt_val}</td>'
    )
    # NV sticky
    nv_val = row.get('Tên NVBH', '')
    if pd.isna(nv_val):
      nv_val = ''
    html.append(
        f'<td style="{sticky_ten_c}{td}background-color:{bg} !important;'
        f'color:{fg} !important;font-weight:{"900" if is_tot else "600"} !important;'
        f'text-align:left !important;">{nv_val}</td>'
    )

    keys = []
    for cat in cats:
      keys.extend([f'{cat}|TARGET', f'{cat}|SELL OUT', f'{cat}|% MTD'])
    keys.extend(['TOTAL|TARGET', 'TOTAL|SELL OUT', 'TOTAL|% MTD'])
    for k in keys:
      val = row.get(k, 0)
      if pd.isna(val):
        val = 0
      is_pct = k.endswith('% MTD')
      if is_pct:
        try:
          disp = f'{int(float(val))}%'
        except Exception:
          disp = str(val)
      else:
        disp = _fmt_perf_num(val, div_million=True)
      if is_tot and not is_pct:
        html.append(
            f'<td class="row-total-cell" style="{tot_s}text-align:right !important;">{disp}</td>'
        )
      elif is_pct:
        # Tháng T: Timegone; tháng trước: mốc 100%
        if use_timegone:
          try:
            _moc = float(_CURRENT_TIMEGONE)
          except Exception:
            _moc = 100.0
        else:
          _moc = 100.0
        cls = color_pct_class(val, moc=_moc)
        bg = color_pct_bg(val, moc=_moc)
        html.append(
            f'<td data-colored="1" class="{cls}" style="{bg}'
            f'text-align:center !important;'
            f'border:1px solid #e2e8f0 !important;padding:3px 4px;font-size:10px;'
            f'font-weight:700 !important;">{disp}</td>'
        )
      else:
        html.append(
            f'<td style="{td}background-color:{bg} !important;color:{fg} !important;'
            f'text-align:right !important;">{disp}</td>'
        )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def build_tea_battle_summary(df_detail):
  """Tổng hợp theo NV + % Chưa Đạt/Tổng KH."""
  cols = [
      'STT', 'Tên NVBH', 'Tổng KH', 'Đã Đạt', 'Chưa Đạt',
      '% Chưa Đạt', 'Đã ĐK', 'Chưa ĐK',
  ]
  if df_detail is None or df_detail.empty:
    return pd.DataFrame(columns=cols)
  d = df_detail.copy()
  rows = []
  for nv, g in d.groupby('Tên NVBH'):
    tong = len(g)
    da_dat = int((pd.to_numeric(g['SỐ SUẤT'], errors='coerce').fillna(0) >= 1).sum())
    chua_dat = int((pd.to_numeric(g['MTD TEA [Thùng]'], errors='coerce').fillna(0) < 10).sum())
    da_dk = int(g['ĐK D&L'].astype(str).str.strip().isin(['✓', '✔']).sum())
    chua_dk = tong - da_dk
    pct_chua = round(chua_dat / tong * 100, 1) if tong else 0.0
    rows.append({
        'Tên NVBH': nv,
        'Tổng KH': tong,
        'Đã Đạt': da_dat,
        'Chưa Đạt': chua_dat,
        '% Chưa Đạt': pct_chua,
        'Đã ĐK': da_dk,
        'Chưa ĐK': chua_dk,
    })
  out = pd.DataFrame(rows).sort_values('Tên NVBH').reset_index(drop=True)
  tong_all = int(out['Tổng KH'].sum())
  chua_all = int(out['Chưa Đạt'].sum())
  tot = {
      'Tên NVBH': 'TỔNG CỘNG',
      'Tổng KH': tong_all,
      'Đã Đạt': int(out['Đã Đạt'].sum()),
      'Chưa Đạt': chua_all,
      '% Chưa Đạt': round(chua_all / tong_all * 100, 1) if tong_all else 0.0,
      'Đã ĐK': int(out['Đã ĐK'].sum()),
      'Chưa ĐK': int(out['Chưa ĐK'].sum()),
  }
  out = pd.concat([out, pd.DataFrame([tot])], ignore_index=True)
  out.insert(0, 'STT', [
      str(i + 1) if i < len(out) - 1 else '-' for i in range(len(out))
  ])
  return out


def render_tea_battle_summary_html(df):
  if df is None or df.empty:
    return ''
  cols = [
      'STT', 'Tên NVBH', 'Tổng KH', 'Đã Đạt', 'Chưa Đạt',
      '% Chưa Đạt', 'Đã ĐK', 'Chưa ĐK',
  ]
  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:8px 6px;font-size:12px;'
  )
  td = (
      'border:1px solid #bce2f5 !important;padding:6px 5px;font-size:12px;'
      'text-align:center !important;'
  )
  tot_s = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;border:1px solid #2b6cb0 !important;'
      'padding:6px 5px;font-size:12px;'
  )
  chua_vals = []
  for _, r in df.iterrows():
    if 'TỔNG' in str(r.get('Tên NVBH', '')).upper():
      continue
    try:
      chua_vals.append(float(r.get('Chưa Đạt', 0) or 0))
    except Exception:
      pass
  vmin = min(chua_vals) if chua_vals else 0.0
  vmax = max(chua_vals) if chua_vals else 1.0
  if vmax <= vmin:
    vmax = vmin + 1.0

  def _chua_cls(v):
    try:
      t = (float(v) - vmin) / (vmax - vmin)
    except Exception:
      t = 0.5
    t = max(0.0, min(1.0, t))
    if t <= 0.33:
      return 'chua-low'
    if t <= 0.66:
      return 'chua-mid'
    return 'chua-high'

  def _pct_chua_class(v):
    try:
      return color_pct_class(100.0 - float(v), moc=100.0)
    except Exception:
      return ''

  html = [
      '<div style="overflow-x:auto;margin:8px 0 16px 0;">',
      '<h4 style="color:#1a365d;font-weight:800;margin:0 0 6px 0;">'
      '📊 TỔNG HỢP THEO NHÂN VIÊN (RR BEV ≥ 3 triệu)</h4>',
      '<table class="custom-kpi-table" style="border-collapse:collapse;'
      'width:100%;min-width:760px;font-family:Arial,sans-serif;"><thead><tr>',
  ]
  for c in cols:
    html.append(f'<th style="{th}">{c}</th>')
  html.append('</tr></thead><tbody>')
  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    bg = '#1a365d' if is_tot else ('#e6f4fc' if pos % 2 == 0 else '#ffffff')
    fg = '#ffffff' if is_tot else '#1a202c'
    html.append('<tr class="row-total">' if is_tot else '<tr>')
    for c in cols:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      al = 'left' if c == 'Tên NVBH' else 'center'
      if c == '% Chưa Đạt' and val != '':
        try:
          disp = f'{float(val):.1f}%'
        except Exception:
          disp = str(val)
      else:
        disp = val

      if c == '% Chưa Đạt':
        cls = _pct_chua_class(val)
        html.append(
            f'<td data-colored="1" class="{cls}" style="text-align:center !important;'
            f'border:1px solid #bce2f5 !important;padding:6px 5px;font-size:12px;'
            f'font-weight:800 !important;">{disp}</td>'
        )
      elif is_tot:
        html.append(
            f'<td class="row-total-cell" style="{tot_s}text-align:{al} !important;">{disp}</td>'
        )
      else:
        html.append(
            f'<td style="{td}background-color:{bg} !important;color:{fg} !important;'
            f'text-align:{al} !important;">{disp}</td>'
        )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)



def load_display_data():
  """Load DANH_SACH_KET_QUA_CUA_HANG_THAM_GIA_CHUONG_TRINH.xlsx"""
  empty = pd.DataFrame()
  candidates = [
      globals().get('DISPLAY_PATH') or os.path.join(
          DATA_DIR, 'DANH_SACH_KET_QUA_CUA_HANG_THAM_GIA_CHUONG_TRINH.xlsx'
      ),
  ]
  if os.path.isdir(get_data_dir()):
    try:
      for fn in os.listdir(get_data_dir()):
        low = fn.lower().replace(' ', '').replace('_', '')
        if fn.lower().endswith(('.xlsx', '.xls')) and (
            'trungbay' in low or 'chuongtrinh' in low
            or 'ketquacuahang' in low or 'danhsachketqua' in low
        ):
          candidates.append(os.path.join(get_data_dir(), fn))
    except Exception:
      pass
  path_use = next((p for p in candidates if p and os.path.isfile(p)), None)
  if not path_use:
    return empty
  try:
    df = pd.read_excel(path_use, header=2)
    if 'Nhân viên BH' not in df.columns and 'Mã CH' not in df.columns:
      df = pd.read_excel(path_use, header=0)
    df.columns = [str(c).strip() for c in df.columns]
    return df
  except Exception:
    try:
      return pd.read_excel(path_use)
    except Exception:
      return empty


def _short_program_name(name):
  s = str(name or '').strip()
  if not s or s.lower() == 'nan':
    return ''
  for pref in ('MSC_', 'MSJ_', 'MSC ', 'MSJ '):
    if s.startswith(pref):
      s = s[len(pref):]
  import re as _re
  s = _re.sub(r'_?HCM_All\d{4}_T\d+', '', s)
  s = _re.sub(r'_+', ' ', s).strip()
  if len(s) > 42:
    s = s[:40] + '…'
  return s



def _resolve_bo_hinh_path():
  names = [
      'DanhSachXetBoHinhTrungBay.xlsx',
      'DanhSachXetBoHinhTrungBay.xls',
      'Danh_Sach_Xet_Bo_Hinh_Trung_Bay.xlsx',
  ]
  for n in names:
    p = os.path.join(get_data_dir(), n)
    if os.path.isfile(p):
      return p
  if os.path.isdir(get_data_dir()):
    for fn in os.listdir(get_data_dir()):
      low = fn.lower().replace(' ', '').replace('_', '')
      if fn.lower().endswith(('.xlsx', '.xls')) and (
          'bohinh' in low or 'xetbohinh' in low
          or ('trungbay' in low and 'xet' in low)
      ):
        return os.path.join(get_data_dir(), fn)
  return os.path.join(get_data_dir(), 'DanhSachXetBoHinhTrungBay.xlsx')


@st.cache_data(ttl=600)
def load_bo_hinh_data():
  """Load DanhSachXetBoHinhTrungBay.xlsx — danh sách bộ hình đã chụp."""
  path = _resolve_bo_hinh_path()
  if not os.path.isfile(path):
    return pd.DataFrame()
  try:
    raw = pd.read_excel(path, header=None, dtype=object)
    header_row = 0
    for i in range(min(8, len(raw))):
      vals = [str(x).strip().lower() for x in raw.iloc[i].tolist() if pd.notna(x)]
      joined = ' | '.join(vals)
      if 'mã cửa hàng' in joined or 'người đăng hình' in joined or 'tên bộ hình' in joined:
        header_row = i
        break
    cols = [
        str(c).strip() if pd.notna(c) else f'Col_{i}'
        for i, c in enumerate(raw.iloc[header_row].tolist())
    ]
    df = raw.iloc[header_row + 1:].copy()
    df.columns = cols
    df = df.dropna(how='all')
    return df
  except Exception:
    return pd.DataFrame()


def build_tb_discipline_maps(df_disp, df_bohinh, df_visit_day, report_date, df_mcp=None):
  """Maps NV → so_ch_tb_per, chup_hinh_ddkd.

  Số CH TB PER:
    CH đăng ký TB chỉ 6 CT permanent Đại sứ (Hóa mỹ phẩm, Gia Vị, Mì, Nước giải khát, Thịt chế biến, Cà phê) ∩
    (lịch VT ngày BC của NV  ∪  CH có Thứ VT 25/36/47 khớp ngày BC trên MCP).

  Chụp hình bởi ĐDKD:
    - Ngày đăng hình = ngày BC
    - Người đăng hình trùng đúng Tên NVBH (không khớp → bỏ, = 0)
    - Tên CT thuộc 6 CT permanent Đại sứ
    - Mã CH ∈ ĐK TB và ∈ lịch VT ngày (gồm 25/36/47)
    → đếm unique Mã CH
  """
  per_map, chup_map = {}, {}
  rd = report_date.date() if hasattr(report_date, 'date') else report_date

  def _nma(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  def _is_allowed_ct(ct):
    """Chỉ đếm đúng 6 CT permanent Đại sứ ngành hàng (whitelist chặt).

    1. MSC_Cuộc thi ảnh Đại sứ Ngành hàng Hóa mỹ phẩm
    2. MSC_Cuộc thi ảnh Đại sứ Ngành hàng Gia Vị
    3. MSC_Cuộc thi ảnh Đại sứ Ngành hàng Mì
    4. MSC_BEV_Cuộc thi ảnh Đại sứ ngành hàng Nước giải khát
    5. MSJ_Cuộc thi ảnh Đại sứ Ngành hàng Thịt chế biến
    6. MSC_POW_Cuộc thi ảnh Đại sứ Ngành hàng Cà phê

    Loại: Sampling, Tích Lũy, TBTN, Khách hàng trọng điểm, và mọi CT khác.
    """
    s = str(ct or '').lower().replace('_', ' ')
    s = ' '.join(s.split())  # normalize spaces

    # Loại rõ ràng
    deny = [
        'trọng điểm', 'trong diem',
        'sampling', 'tbtn',
        'tích lũy', 'tich luy', 'tichluy', 'tích luỹ',
    ]
    for d in deny:
      if d in s:
        return False

    # Bắt buộc có "đại sứ" (không chỉ "cuộc thi ảnh")
    if 'đại sứ' not in s and 'dai su' not in s:
      return False

    # Phải khớp 1 trong 6 ngành
    industries = [
        ('hóa mỹ phẩm', 'hoa my pham'),
        ('gia vị', 'gia vi'),
        ('nước giải khát', 'nuoc giai khat'),
        ('thịt chế biến', 'thit che bien'),
        ('cà phê', 'ca phe'),
        # Mì: tránh match nhầm — yêu cầu "mì" gần "ngành hàng" hoặc đứng sau đại sứ
        ('ngành hàng mì', 'nganh hang mi'),
        ('đại sứ ngành hàng mì', 'dai su nganh hang mi'),
    ]
    for pair in industries:
      for kw in pair:
        if kw in s:
          return True

    # Fallback riêng cho Mì: "đại sứ" + " mì" / " mi " (word boundary-ish)
    if (' mì' in s or s.endswith(' mì') or ' mi ' in s or s.endswith(' mi')
            or 'hàng mì' in s or 'hang mi' in s):
      if 'đại sứ' in s or 'dai su' in s:
        return True

    return False

  def _is_excluded_ct(ct):
    # True = loại bỏ (không thuộc 6 CT whitelist)
    return not _is_allowed_ct(ct)

  # Thứ trong tuần: Mon=2 ... Sat=7 (CN bỏ)
  try:
    wd = rd.weekday()  # Mon=0
    day_code = str(wd + 2) if wd <= 5 else None  # Mon→2 ... Sat→7
  except Exception:
    day_code = None
  # Code VT hợp lệ cho ngày hôm nay
  valid_thu = set()
  if day_code:
    valid_thu.add(day_code)
    if day_code in ('2', '5'):
      valid_thu.add('25')
    if day_code in ('3', '6'):
      valid_thu.add('36')
    if day_code in ('4', '7'):
      valid_thu.add('47')

  # Lịch VT ngày từ file lịch: nv → set mã CH
  vt_by_nv = {}
  if df_visit_day is not None and not df_visit_day.empty:
    vis = df_visit_day.copy()
    c_nv = find_col(vis, ['Tên NVBH', 'NVBH']) or (
        '_nv' if '_nv' in vis.columns else None
    )
    c_ma = find_col(vis, ['Mã Cửa hàng', 'Mã CH', 'Outlet_code']) or (
        '_ma' if '_ma' in vis.columns else None
    )
    if c_nv and c_ma:
      for _, r in vis.iterrows():
        nv = str(r[c_nv]).strip()
        ma = _nma(r[c_ma])
        if not nv or not ma or ma.lower() in ('nan', 'none'):
          continue
        vt_by_nv.setdefault(nv, set()).add(ma)

  # Bổ sung CH có Thứ / Thứ VT (25/36/47) khớp ngày BC từ MCP
  if df_mcp is not None and not getattr(df_mcp, 'empty', True) and valid_thu:
    c_nv = find_col(df_mcp, [
        'SM name', 'SM NAME', 'Tên NVBH', 'NVBH', 'Nhân viên', 'SM_NAME',
    ])
    c_ma = find_col(df_mcp, [
        'Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH', 'OUTLET_CODE',
    ])
    c_thu = find_col(df_mcp, [
        'Thứ', 'Thứ VT', 'Thu VT', 'THỨ VT', 'THỨ', 'Ngay VT', 'Ngày VT',
    ])
    if c_ma and c_thu:
      for _, r in df_mcp.iterrows():
        thu = str(r[c_thu]).strip().replace('.0', '')
        if thu not in valid_thu:
          continue
        ma = _nma(r[c_ma])
        if not ma or ma.lower() in ('nan', 'none'):
          continue
        nv = str(r[c_nv]).strip() if c_nv and pd.notna(r.get(c_nv)) else ''
        if not nv:
          continue
        vt_by_nv.setdefault(nv, set()).add(ma)

  known_nvs = set(vt_by_nv.keys())

  # Đăng ký TB trừ Sampling & TBTN
  reg_by_nv = {}
  if df_disp is not None and not df_disp.empty:
    d = df_disp.copy()
    c_nv = find_col(d, ['Nhân viên BH', 'Tên NVBH', 'NVBH'])
    c_ma = find_col(d, ['Mã CH', 'Mã KH', 'Mã cửa hàng'])
    c_ct = find_col(d, ['Tên chương trình', 'Chương trình', 'Tên CT'])
    if c_nv and c_ma:
      for _, r in d.iterrows():
        if c_ct and _is_excluded_ct(r.get(c_ct)):
          continue
        nv = str(r[c_nv]).strip()
        ma = _nma(r[c_ma])
        if not nv or not ma or ma.lower() in ('nan', 'none'):
          continue
        reg_by_nv.setdefault(nv, set()).add(ma)
        known_nvs.add(nv)

  # PER = |reg ∩ plan| (plan đã gồm 25/36/47)
  for nv in known_nvs:
    plan = vt_by_nv.get(nv, set())
    reg = reg_by_nv.get(nv, set())
    per_map[nv] = len(plan & reg) if plan else 0

  # Chụp hình: chỉ khi Người đăng hình trùng đúng Tên NVBH
  if df_bohinh is not None and not df_bohinh.empty:
    b = df_bohinh.copy()
    c_nguoi = find_col(b, ['Người đăng hình', 'Người Đăng Hình'])
    c_ngay = find_col(b, ['Ngày đăng hình', 'Ngày Đăng Hình'])
    c_ma = find_col(b, ['Mã cửa hàng', 'Mã CH', 'Mã KH'])
    c_ct = find_col(b, ['Tên CT', 'Tên chương trình', 'Chương trình'])
    if c_nguoi and c_ngay and c_ma:
      b['_ngay'] = pd.to_datetime(b[c_ngay], errors='coerce').dt.date
      b = b[b['_ngay'] == rd]
      for _, r in b.iterrows():
        if c_ct and _is_excluded_ct(r.get(c_ct)):
          continue
        nguoi = str(r[c_nguoi]).strip()
        # Không trùng tên NV → bỏ (= 0)
        if nguoi not in known_nvs and nguoi not in reg_by_nv and nguoi not in vt_by_nv:
          continue
        if nguoi not in known_nvs:
          # vẫn cho phép nếu là tên NV có trong reg
          if nguoi not in reg_by_nv:
            continue
        ma = _nma(r[c_ma])
        if not ma:
          continue
        plan = vt_by_nv.get(nguoi, set())
        reg = reg_by_nv.get(nguoi, set())
        if ma in plan and ma in reg:
          chup_map.setdefault(nguoi, set()).add(ma)

  chup_cnt = {nv: len(s) for nv, s in chup_map.items()}
  return per_map, chup_cnt



def build_display_report(df_disp, df_mcp=None, filter_nv=None):
  """(df_summary, df_by_prog, df_detail, comments_html)"""
  empty = pd.DataFrame()
  if df_disp is None or df_disp.empty:
    return empty, empty, empty, ''

  d = df_disp.copy()
  c_nv = 'Nhân viên BH' if 'Nhân viên BH' in d.columns else find_col(
      d, ['Nhân viên BH', 'Tên NVBH', 'NVBH']
  )
  c_ma = 'Mã CH' if 'Mã CH' in d.columns else find_col(d, ['Mã CH', 'Mã KH'])
  c_ten = 'Tên cửa hàng' if 'Tên cửa hàng' in d.columns else find_col(
      d, ['Tên cửa hàng', 'Tên KH', 'Tên CH']
  )
  c_ct = 'Tên chương trình' if 'Tên chương trình' in d.columns else find_col(
      d, ['Tên chương trình', 'Chương trình']
  )
  c_muc = 'Mức đăng ký' if 'Mức đăng ký' in d.columns else find_col(
      d, ['Mức đăng ký', 'Mức ĐK']
  )
  c_anh = 'Số bộ ảnh đã chụp' if 'Số bộ ảnh đã chụp' in d.columns else find_col(
      d, ['Số bộ ảnh đã chụp', 'Số bộ ảnh duyệt']
  )
  if not c_nv or not c_ma:
    return empty, empty, empty, ''

  def _norm_ma(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  d['_nv'] = d[c_nv].astype(str).str.strip()
  d['_ma'] = d[c_ma].map(_norm_ma)
  d['_ten'] = d[c_ten].astype(str).str.strip() if c_ten else ''
  d['_ct'] = d[c_ct].astype(str).str.strip() if c_ct else ''
  d['_muc'] = d[c_muc].astype(str).str.strip() if c_muc else ''
  d['_anh'] = (
      pd.to_numeric(d[c_anh], errors='coerce').fillna(0).astype(int)
      if c_anh else 0
  )

  if filter_nv:
    vals = [
        str(v).strip()
        for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])
        if str(v).strip()
    ]
    if vals:
      d = d[d['_nv'].isin(vals)]
  if d.empty:
    return empty, empty, empty, ''

  def _agg(g):
    n_dk = len(g)
    n_chup = int((g['_anh'] >= 1).sum())
    n_chua = int((g['_anh'] < 1).sum())
    n_ge6 = int((g['_anh'] >= 6).sum())
    n_lt6 = int((g['_anh'] < 6).sum())
    return {
        'CH ĐK': n_dk,
        'CH ĐÃ CHỤP': n_chup,
        '% ĐÃ CHỤP': round(n_chup / n_dk * 100, 1) if n_dk else 0.0,
        'CH CHƯA CHỤP': n_chua,
        '% CHƯA CHỤP': round(n_chua / n_dk * 100, 1) if n_dk else 0.0,
        'CH >= 6 BỘ ẢNH': n_ge6,
        '% CH >= 6 BỘ ẢNH': round(n_ge6 / n_dk * 100, 1) if n_dk else 0.0,
        'SỐ CH < 6 BỘ ẢNH': n_lt6,
        '% CH < 6 BỘ ẢNH': round(n_lt6 / n_dk * 100, 1) if n_dk else 0.0,
    }

  rows = []
  for nv, g in d.groupby('_nv', sort=False):
    r = _agg(g)
    r['Tên NVBH'] = nv
    rows.append(r)
  df1 = pd.DataFrame(rows)
  if not df1.empty:
    df1 = df1.sort_values('% CHƯA CHỤP', ascending=False).reset_index(drop=True)
    df1.insert(0, 'STT', range(1, len(df1) + 1))
    tot = {'STT': '-', 'Tên NVBH': 'TỔNG CỘNG', **_agg(d)}
    df1 = pd.concat([df1, pd.DataFrame([tot])], ignore_index=True)

  programs = [p for p in d['_ct'].dropna().unique() if p and str(p).lower() != 'nan']
  rows2 = []
  for nv, gnv in d.groupby('_nv', sort=False):
    row = {'Tên NVBH': nv}
    for prog in programs:
      gp = gnv[gnv['_ct'] == prog]
      short = _short_program_name(prog)
      a = _agg(gp) if not gp.empty else {
          'CH ĐK': 0, 'CH ĐÃ CHỤP': 0, '% ĐÃ CHỤP': 0.0,
          'CH CHƯA CHỤP': 0, 'CH >= 6 BỘ ẢNH': 0,
      }
      row[f'{short}|CH ĐĂNG KÝ'] = a['CH ĐK']
      row[f'{short}|CH ĐÃ CHỤP'] = a['CH ĐÃ CHỤP']
      row[f'{short}|% ĐÃ CHỤP'] = a['% ĐÃ CHỤP']
      row[f'{short}|CHƯA CHỤP'] = a['CH CHƯA CHỤP']
      row[f'{short}|>= 6 BỘ ẢNH'] = a['CH >= 6 BỘ ẢNH']
    rows2.append(row)
  df2 = pd.DataFrame(rows2)
  if not df2.empty:
    df2.insert(0, 'STT', range(1, len(df2) + 1))
    tot2 = {'STT': '-', 'Tên NVBH': 'TỔNG CỘNG'}
    for prog in programs:
      short = _short_program_name(prog)
      gp = d[d['_ct'] == prog]
      a = _agg(gp) if not gp.empty else {
          'CH ĐK': 0, 'CH ĐÃ CHỤP': 0, '% ĐÃ CHỤP': 0.0,
          'CH CHƯA CHỤP': 0, 'CH >= 6 BỘ ẢNH': 0,
      }
      tot2[f'{short}|CH ĐĂNG KÝ'] = a['CH ĐK']
      tot2[f'{short}|CH ĐÃ CHỤP'] = a['CH ĐÃ CHỤP']
      tot2[f'{short}|% ĐÃ CHỤP'] = a['% ĐÃ CHỤP']
      tot2[f'{short}|CHƯA CHỤP'] = a['CH CHƯA CHỤP']
      tot2[f'{short}|>= 6 BỘ ẢNH'] = a['CH >= 6 BỘ ẢNH']
    df2 = pd.concat([df2, pd.DataFrame([tot2])], ignore_index=True)

  # Map Mã KH (display) ↔ Outlet_code (MCP) → cột Thứ
  thu_map = {}
  if df_mcp is not None and not df_mcp.empty:
    mcp = df_mcp.copy()
    mcp.columns = [str(c).strip() for c in mcp.columns]
    c_mcp_ma = None
    for cand in [
        'Outlet_code', 'Outlet Code', 'Outlet code', 'outlet_code',
        'Mã CH', 'Ma CH', 'Mã KH', 'Ma KH', 'Customer Code',
    ]:
      for c in mcp.columns:
        if str(c).strip().lower().replace(' ', '_') == cand.lower().replace(' ', '_'):
          c_mcp_ma = c
          break
        if str(c).strip().lower() == cand.lower():
          c_mcp_ma = c
          break
      if c_mcp_ma:
        break
    if not c_mcp_ma:
      c_mcp_ma = find_col(mcp, [
          'Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH', 'Customer Code', 'Outlet'
      ])
    c_mcp_thu = None
    for c in mcp.columns:
      cl = str(c).strip().lower()
      if cl in ('thứ', 'thu', 'thu vt', 'thứ vt', 'day'):
        c_mcp_thu = c
        break
    if not c_mcp_thu:
      c_mcp_thu = find_col(mcp, ['Thứ', 'Thu', 'Day', 'Tần suất', 'Frequency'])

    if c_mcp_ma and c_mcp_thu:
      for _, r in mcp.iterrows():
        ma = _norm_ma(r[c_mcp_ma])
        if not ma:
          continue
        thu_val = r[c_mcp_thu]
        if pd.isna(thu_val):
          continue
        # giữ nguyên mã 25/36/47 hoặc số 2..7
        try:
          if isinstance(thu_val, float) and thu_val == int(thu_val):
            thu_s = str(int(thu_val))
          else:
            thu_s = str(thu_val).strip()
            if thu_s.endswith('.0'):
              thu_s = thu_s[:-2]
        except Exception:
          thu_s = str(thu_val).strip()
        thu_map[ma] = thu_s
        # thêm alias không leading zero / int form
        try:
          thu_map[str(int(float(ma)))] = thu_s
        except Exception:
          pass

  def _lookup_thu(m):
    if m in thu_map:
      return thu_map[m]
    try:
      return thu_map.get(str(int(float(m))), '')
    except Exception:
      return ''

  df3 = pd.DataFrame({
      'Tên NVBH': d['_nv'].values,
      'Mã KH': d['_ma'].values,
      'Tên KH': d['_ten'].values,
      'Tên Chương Trình TB': d['_ct'].values,
      'Mức ĐK': d['_muc'].values,
      'Số Bộ Ảnh Đã Chụp': d['_anh'].values,
      'Thứ VT': d['_ma'].map(_lookup_thu).values,
  })

  comments = ''
  if not df1.empty:
    body = df1[df1['STT'].astype(str) != '-'].copy()
    if not body.empty:
      b1 = body.sort_values('% CHƯA CHỤP', ascending=False).head(3)
      b2 = body.sort_values('% CH < 6 BỘ ẢNH', ascending=False).head(3)
      lines = [
          '<div class="note-box" style="margin-top:14px;">',
          '<b>📝 NHẬN XÉT HIỆU SUẤT TRƯNG BÀY</b><br/><br/>',
          '<b style="color:#034ea2;">1. Bottom 3 % CH chưa chụp cao nhất</b><br/>',
      ]
      for _, r in b1.iterrows():
        lines.append(
            f"• {r['Tên NVBH']}: <b style='color:#c53030;'>{r['% CHƯA CHỤP']:.1f}%</b> "
            f"({int(r['CH CHƯA CHỤP'])}/{int(r['CH ĐK'])} CH)<br/>"
        )
      lines.append(
          '<br/><b style="color:#034ea2;">2. Bottom 3 % CH &lt; 6 bộ ảnh cao nhất</b><br/>'
      )
      for _, r in b2.iterrows():
        lines.append(
            f"• {r['Tên NVBH']}: <b style='color:#c53030;'>{r['% CH < 6 BỘ ẢNH']:.1f}%</b> "
            f"({int(r['SỐ CH < 6 BỘ ẢNH'])}/{int(r['CH ĐK'])} CH)<br/>"
        )
      lines.append('</div>')
      comments = ''.join(lines)

  return df1, df2, df3, comments


def _disp_pct_style(col_name, v):
  """Tô màu % trưng bày: đã chụp/>=6 cao=tốt; chưa chụp/<6 cao=xấu.
  Dùng cùng palette KPI (đỏ/xanh/tím)."""
  try:
    v = float(str(v).replace('%', '').strip())
  except Exception:
    return '', ''
  red = 'background-color:#fed7d7 !important;color:#742a2a !important;font-weight:800 !important;'
  green = 'background-color:#c6f6d5 !important;color:#22543d !important;font-weight:800 !important;'
  purple = 'background-color:#e9d8fd !important;color:#553c9a !important;font-weight:800 !important;'
  c = str(col_name)
  # Cột xấu khi cao
  if 'CHƯA' in c or '< 6' in c or 'CHUA' in c.upper():
    # map: cao % chưa chụp = đỏ. Dùng mốc 100: v cao → đỏ
    score = 100.0 - v  # thấp score = xấu
    if score < 50:
      return 'pct-red', red
    if score < 80:
      return 'pct-green', green
    return 'pct-purple', purple
  # Cột tốt khi cao (đã chụp, >=6)
  if v < 50:
    return 'pct-red', red
  if v < 80:
    return 'pct-green', green
  return 'pct-purple', purple



def rebuild_display_summary(
    df_disp, mcp=None, filter_nv=None, filter_thu=None, filter_nv_list=None, filter_prog=None
):
  """Build bảng 1 (tổng hợp NV) với lọc Chương trình / Thứ VT / Tên NVBH."""
  empty = pd.DataFrame()
  if df_disp is None or df_disp.empty:
    return empty

  d = df_disp.copy()
  c_nv = find_col(d, ['Nhân viên BH', 'Tên NVBH', 'NVBH'])
  c_ma = find_col(d, ['Mã CH', 'Mã KH', 'Mã cửa hàng'])
  c_ct = find_col(d, ['Tên chương trình', 'Chương trình', 'Tên CT'])
  c_anh = find_col(d, ['Số bộ ảnh đã chụp', 'Số bộ ảnh duyệt'])
  if not c_nv or not c_ma:
    return empty

  def _nma(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  d['_nv'] = d[c_nv].astype(str).str.strip()
  d['_ma'] = d[c_ma].map(_nma)
  d['_ct'] = d[c_ct].astype(str).str.strip() if c_ct else ''
  d['_anh'] = (
      pd.to_numeric(d[c_anh], errors='coerce').fillna(0).astype(int)
      if c_anh else 0
  )

  if nv_selected(filter_nv):
    vals = filter_nv if isinstance(filter_nv, list) else [filter_nv]
    d = d[d['_nv'].isin([str(v).strip() for v in vals])]

  if filter_nv_list:
    d = d[d['_nv'].isin([str(v).strip() for v in filter_nv_list])]

  if filter_prog:
    # khớp full name hoặc short name
    prog_sel = [str(p).strip() for p in filter_prog if str(p).strip()]
    if prog_sel:
      def _match_prog(ct):
        ct = str(ct).strip()
        if ct in prog_sel:
          return True
        short = _short_program_name(ct) if ct else ''
        return short in prog_sel
      d = d[d['_ct'].map(_match_prog)]

  # Map CH → Thứ từ MCP
  thu_map = {}
  if mcp is not None and not getattr(mcp, 'empty', True):
    c_m = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH'])
    c_t = find_col(mcp, ['Thứ', 'Thứ VT', 'Thu VT', 'THỨ'])
    if c_m and c_t:
      for _, r in mcp.iterrows():
        ma = _nma(r[c_m])
        if ma:
          thu_map[ma] = str(r[c_t]).strip()

  if filter_thu:
    thu_sel = set(str(t).strip() for t in filter_thu if str(t).strip())
    if thu_sel and thu_map:
      def _ok_thu(ma):
        t = str(thu_map.get(str(ma).strip(), '')).strip()
        if not t:
          return False
        if t in thu_sel:
          return True
        # match single digit in codes like 25/36/47
        for code in thu_sel:
          if code in t or t in code:
            return True
        return False
      d = d[d['_ma'].map(_ok_thu)]

  if d.empty:
    return empty

  def _agg(g):
    n_dk = len(g)
    n_chup = int((g['_anh'] >= 1).sum())
    n_chua = int((g['_anh'] < 1).sum())
    n_ge6 = int((g['_anh'] >= 6).sum())
    n_lt6 = int((g['_anh'] < 6).sum())
    return {
        'CH ĐK': n_dk,
        'CH ĐÃ CHỤP': n_chup,
        '% ĐÃ CHỤP': round(n_chup / n_dk * 100, 1) if n_dk else 0.0,
        'CH CHƯA CHỤP': n_chua,
        '% CHƯA CHỤP': round(n_chua / n_dk * 100, 1) if n_dk else 0.0,
        'CH >= 6 BỘ ẢNH': n_ge6,
        '% CH >= 6 BỘ ẢNH': round(n_ge6 / n_dk * 100, 1) if n_dk else 0.0,
        'SỐ CH < 6 BỘ ẢNH': n_lt6,
        '% CH < 6 BỘ ẢNH': round(n_lt6 / n_dk * 100, 1) if n_dk else 0.0,
    }

  rows = []
  for nv, g in d.groupby('_nv', sort=False):
    r = _agg(g)
    r['Tên NVBH'] = nv
    rows.append(r)
  df1 = pd.DataFrame(rows)
  if df1.empty:
    return empty
  df1 = df1.sort_values('% CHƯA CHỤP', ascending=False).reset_index(drop=True)
  df1.insert(0, 'STT', range(1, len(df1) + 1))
  tot = {'STT': '-', 'Tên NVBH': 'TỔNG CỘNG', **_agg(d)}
  df1 = pd.concat([df1, pd.DataFrame([tot])], ignore_index=True)
  return df1


def rebuild_display_by_program(
    df_disp, mcp=None, filter_nv=None, filter_thu=None, filter_nv_list=None, filter_prog=None
):
  """Build bảng 2 (chi tiết theo CT) với lọc Thứ VT / NV / Chương trình.

  filter_thu: list mã thứ ('2','3',..,'25','36','47') — CH phải khớp MCP Thứ.
  Số liệu CH ĐK / Đã chụp tính lại theo CH thỏa điều kiện.
  Dòng TOTAL = tổng theo dữ liệu đang lọc.
  """
  empty = pd.DataFrame()
  if df_disp is None or df_disp.empty:
    return empty

  d = df_disp.copy()
  c_nv = find_col(d, ['Nhân viên BH', 'Tên NVBH', 'NVBH'])
  c_ma = find_col(d, ['Mã CH', 'Mã KH', 'Mã cửa hàng'])
  c_ct = find_col(d, ['Tên chương trình', 'Chương trình', 'Tên CT'])
  c_anh = find_col(d, ['Số bộ ảnh đã chụp', 'Số bộ ảnh duyệt'])
  if not c_nv or not c_ma or not c_ct:
    return empty

  def _nma(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  d['_nv'] = d[c_nv].astype(str).str.strip()
  d['_ma'] = d[c_ma].map(_nma)
  d['_ct'] = d[c_ct].astype(str).str.strip()
  d['_anh'] = pd.to_numeric(d[c_anh], errors='coerce').fillna(0) if c_anh else 0

  if nv_selected(filter_nv):
    vals = filter_nv if isinstance(filter_nv, list) else [filter_nv]
    d = d[d['_nv'].isin([str(v).strip() for v in vals])]

  if filter_nv_list:
    d = d[d['_nv'].isin([str(v).strip() for v in filter_nv_list])]

  # Map CH → Thứ từ MCP
  thu_map = {}
  if mcp is not None and not getattr(mcp, 'empty', True):
    c_m = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH'])
    c_t = find_col(mcp, ['Thứ', 'Thứ VT', 'Thu VT', 'THỨ'])
    if c_m and c_t:
      for _, r in mcp.iterrows():
        ma = _nma(r[c_m])
        if ma:
          thu_map[ma] = str(r[c_t]).strip().replace('.0', '')

  d['_thu'] = d['_ma'].map(lambda x: thu_map.get(x, ''))

  # Lọc Thứ VT (hỗ trợ 25/36/47)
  if filter_thu:
    thu_list = [str(t).strip() for t in filter_thu if str(t).strip()]
    if thu_list:
      mapping_rules = {
          '2': {'2', '25'}, '3': {'3', '36'}, '4': {'4', '47'},
          '5': {'5', '25'}, '6': {'6', '36'}, '7': {'7', '47'},
          '25': {'25'}, '36': {'36'}, '47': {'47'},
      }
      valid = set()
      for t in thu_list:
        valid |= mapping_rules.get(t, {t})
      # CH có Thứ ∈ valid; CH không map Thứ → loại khi đang lọc
      d = d[d['_thu'].isin(valid)]

  if filter_prog:
    # filter_prog là short name hoặc full name
    def _match_prog(ct):
      short = _short_program_name(ct)
      return short in filter_prog or ct in filter_prog
    d = d[d['_ct'].map(_match_prog)]

  if d.empty:
    return empty

  def _agg(g):
    n_dk = g['_ma'].nunique() if len(g) else 0
    # unique CH đã chụp (>=1 ảnh) — lấy max ảnh theo CH
    if len(g):
      by_ch = g.groupby('_ma')['_anh'].max()
      n_chup = int((by_ch >= 1).sum())
      n_chua = int((by_ch < 1).sum())
      n_ge6 = int((by_ch >= 6).sum())
    else:
      n_chup = n_chua = n_ge6 = 0
    return {
        'CH ĐK': n_dk,
        'CH ĐÃ CHỤP': n_chup,
        '% ĐÃ CHỤP': round(n_chup / n_dk * 100, 1) if n_dk else 0.0,
        'CH CHƯA CHỤP': n_chua,
        'CH >= 6 BỘ ẢNH': n_ge6,
    }

  programs = [p for p in d['_ct'].dropna().unique() if p and str(p).lower() != 'nan']
  # giữ thứ tự program gốc nếu có
  rows2 = []
  for nv, gnv in d.groupby('_nv', sort=False):
    row = {'Tên NVBH': nv}
    for prog in programs:
      gp = gnv[gnv['_ct'] == prog]
      short = _short_program_name(prog)
      a = _agg(gp)
      row[f'{short}|CH ĐĂNG KÝ'] = a['CH ĐK']
      row[f'{short}|CH ĐÃ CHỤP'] = a['CH ĐÃ CHỤP']
      row[f'{short}|% ĐÃ CHỤP'] = a['% ĐÃ CHỤP']
      row[f'{short}|CHƯA CHỤP'] = a['CH CHƯA CHỤP']
      row[f'{short}|>= 6 BỘ ẢNH'] = a['CH >= 6 BỘ ẢNH']
    rows2.append(row)
  df2 = pd.DataFrame(rows2)
  if df2.empty:
    return empty
  df2.insert(0, 'STT', range(1, len(df2) + 1))
  # TOTAL theo dữ liệu đang lọc
  tot2 = {'STT': '-', 'Tên NVBH': 'TỔNG CỘNG'}
  for prog in programs:
    short = _short_program_name(prog)
    a = _agg(d[d['_ct'] == prog])
    tot2[f'{short}|CH ĐĂNG KÝ'] = a['CH ĐK']
    tot2[f'{short}|CH ĐÃ CHỤP'] = a['CH ĐÃ CHỤP']
    tot2[f'{short}|% ĐÃ CHỤP'] = a['% ĐÃ CHỤP']
    tot2[f'{short}|CHƯA CHỤP'] = a['CH CHƯA CHỤP']
    tot2[f'{short}|>= 6 BỘ ẢNH'] = a['CH >= 6 BỘ ẢNH']
  df2 = pd.concat([df2, pd.DataFrame([tot2])], ignore_index=True)
  return df2



def render_display_summary_html(df):
  """Bảng 1: sticky STT + Tên NVBH + header; % tô màu; total row-total."""
  if df is None or df.empty:
    return '<p>Không có dữ liệu trưng bày.</p>'
  cols = [
      'STT', 'Tên NVBH', 'CH ĐK', 'CH ĐÃ CHỤP', '% ĐÃ CHỤP',
      'CH CHƯA CHỤP', '% CHƯA CHỤP', 'CH >= 6 BỘ ẢNH', '% CH >= 6 BỘ ẢNH',
      'SỐ CH < 6 BỘ ẢNH', '% CH < 6 BỘ ẢNH',
  ]
  max_name = 12
  if 'Tên NVBH' in df.columns:
    for n in df['Tên NVBH'].astype(str):
      max_name = max(max_name, len(n))
  name_w = max(140, min(280, max_name * 9 + 24))

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 5px;font-size:11px;'
  )
  th_g = (
      'background-color:#f6e05e !important;color:#1a365d !important;'
      'font-weight:900 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:8px;font-size:13px;'
  )
  td = 'border:1px solid #bce2f5 !important;padding:5px 4px;font-size:12px;'
  tot_style = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;border:1px solid #2b6cb0 !important;'
      'padding:5px 4px;font-size:12px;'
  )
  sticky_stt_h = (
      f'{th}position:sticky;left:0;z-index:6;min-width:44px;max-width:44px;'
  )
  sticky_ten_h = (
      f'{th}position:sticky;left:44px;z-index:6;min-width:{name_w}px;'
  )
  sticky_stt_c = 'position:sticky;left:0;z-index:2;min-width:44px;max-width:44px;'
  sticky_ten_c = f'position:sticky;left:44px;z-index:2;min-width:{name_w}px;'

  # Sticky group header "THÔNG TIN ĐDKD" spans STT + Tên NVBH
  sticky_group = (
      f'{th_g}position:sticky;left:0;z-index:7;'
      f'min-width:{44 + name_w}px;'
  )
  html = [
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;'
      'width:max-content;min-width:100%;font-family:Arial,sans-serif;">',
      '<thead style="position:sticky;top:0;z-index:5;">',
      f'<tr><th colspan="2" style="{sticky_group}">THÔNG TIN ĐDKD</th>'
      f'<th colspan="9" style="{th_g}">HIỆU SUẤT TRƯNG BÀY</th></tr>',
      '<tr>',
      f'<th style="{sticky_stt_h}">STT</th>',
      f'<th style="{sticky_ten_h}">Tên NVBH</th>',
  ]
  for c in cols[2:]:
    html.append(f'<th style="{th}">{c}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = (
        str(row.get('STT', '')).strip() in ('-', 'TOTAL')
        or 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    )
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    tr_cls = ' class="row-total"' if is_tot else ''
    html.append(f'<tr{tr_cls}>')
    for c in cols:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      sticky = ''
      if c == 'STT':
        sticky = sticky_stt_c
      elif c == 'Tên NVBH':
        sticky = sticky_ten_c

      if c.startswith('%'):
        try:
          v = float(str(val).replace('%', '').strip())
          val_s = f'{v:.1f}%'
        except Exception:
          v, val_s = 0.0, str(val)
        if is_tot:
          html.append(
              f'<td class="row-total-cell" style="{tot_style}{sticky}'
              f'text-align:center !important;">{val_s}</td>'
          )
        else:
          cls, style_bg = _disp_pct_style(c, v)
          html.append(
              f'<td data-colored="1" class="{cls}" style="{td}{style_bg}{sticky}'
              f'text-align:center;">{val_s}</td>'
          )
      else:
        al = 'left' if c == 'Tên NVBH' else 'center'
        if is_tot:
          html.append(
              f'<td class="row-total-cell" style="{tot_style}{sticky}'
              f'text-align:{al} !important;white-space:nowrap;">{val}</td>'
          )
        else:
          html.append(
              f'<td style="{td}{sticky}background:{bg} !important;color:#1a202c !important;'
              f'font-weight:400;text-align:{al};white-space:nowrap;">{val}</td>'
          )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)


def render_display_by_program_html(df):
  """Bảng 2: sticky STT + Tên NVBH + 2 dòng header; chỉ cuộn ngang; % tô màu rule KPI."""
  if df is None or df.empty:
    return ''
  prog_cols = [c for c in df.columns if '|' in str(c)]
  groups = {}
  for c in prog_cols:
    prog, metric = str(c).split('|', 1)
    groups.setdefault(prog, []).append((c, metric))

  # độ rộng cột tên theo tên dài nhất
  max_name = 12
  if 'Tên NVBH' in df.columns:
    for n in df['Tên NVBH'].astype(str):
      max_name = max(max_name, len(n))
  name_w = max(140, min(280, max_name * 9 + 24))

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:5px 3px;font-size:10px;'
  )
  th_y = (
      'background-color:#f6e05e !important;color:#1a365d !important;'
      'font-weight:900 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 3px;font-size:11px;'
  )
  td = 'border:1px solid #bce2f5 !important;padding:4px 3px;font-size:11px;'
  sticky_base = 'position:sticky;z-index:3;background:#1a365d !important;color:#fff !important;'
  sticky_stt = sticky_base + 'left:0;min-width:44px;max-width:44px;'
  sticky_ten_h = sticky_base + f'left:44px;min-width:{name_w}px;z-index:4;'
  sticky_stt_cell = (
      f'position:sticky;left:0;z-index:2;min-width:44px;max-width:44px;'
  )
  sticky_ten_cell = (
      f'position:sticky;left:44px;z-index:2;min-width:{name_w}px;'
  )

  html = [
      '<div style="overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;'
      'margin-top:16px;max-width:100%;">',
      '<h4 style="color:#1a365d;font-weight:800;margin:8px 0 6px 0;">'
      '📋 CHI TIẾT THEO TỪNG CHƯƠNG TRÌNH TRƯNG BÀY</h4>',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;'
      'width:max-content;min-width:100%;font-family:Arial,sans-serif;">',
      '<thead style="position:sticky;top:0;z-index:5;">',
      f'<tr><th rowspan="2" style="{th}{sticky_stt}">STT</th>'
      f'<th rowspan="2" style="{th}{sticky_ten_h}">Tên NVBH</th>',
  ]
  for prog, metrics in groups.items():
    html.append(f'<th colspan="{len(metrics)}" style="{th_y}">{prog}</th>')
  html.append('</tr><tr>')
  for _, metrics in groups.items():
    for _, metric in metrics:
      html.append(f'<th style="{th}">{metric}</th>')
  html.append('</tr></thead><tbody>')

  tot_style = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:900 !important;border:1px solid #2b6cb0 !important;'
      'padding:4px 3px;font-size:11px;'
  )
  for pos, (_, row) in enumerate(df.iterrows()):
    is_tot = (
        str(row.get('STT', '')).strip() in ('-', 'TOTAL')
        or 'TỔNG' in str(row.get('Tên NVBH', '')).upper()
    )
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    fg = '#1a202c'
    fw = '400'
    tr_cls = ' class="row-total"' if is_tot else ''
    html.append(f'<tr{tr_cls}>')
    if is_tot:
      html.append(
          f'<td class="row-total-cell" style="{tot_style}{sticky_stt_cell}'
          f'text-align:center !important;">{row.get("STT","")}</td>'
      )
      html.append(
          f'<td class="row-total-cell" style="{tot_style}{sticky_ten_cell}'
          f'text-align:left !important;white-space:nowrap;">'
          f'{row.get("Tên NVBH","")}</td>'
      )
    else:
      html.append(
          f'<td style="{td}{sticky_stt_cell}background:{bg} !important;'
          f'color:{fg} !important;text-align:center;font-weight:{fw};">'
          f'{row.get("STT","")}</td>'
      )
      html.append(
          f'<td style="{td}{sticky_ten_cell}background:{bg} !important;'
          f'color:{fg} !important;text-align:left;font-weight:{fw};'
          f'white-space:nowrap;">{row.get("Tên NVBH","")}</td>'
      )
    for _, metrics in groups.items():
      for col, metric in metrics:
        val = row.get(col, 0)
        if pd.isna(val):
          val = 0
        if metric.startswith('%'):
          try:
            v = float(str(val).replace('%', '').strip())
            val_s = f'{v:.1f}%'
          except Exception:
            v, val_s = 0.0, str(val)
          if is_tot:
            html.append(
                f'<td class="row-total-cell" style="{tot_style}'
                f'text-align:center !important;">{val_s}</td>'
            )
          else:
            cls, style_bg = _disp_pct_style(metric, v)
            html.append(
                f'<td data-colored="1" class="{cls}" style="{td}{style_bg}'
                f'text-align:center;">{val_s}</td>'
            )
        else:
          try:
            val_s = str(int(val))
          except Exception:
            val_s = str(val)
          if is_tot:
            html.append(
                f'<td class="row-total-cell" style="{tot_style}'
                f'text-align:center !important;">{val_s}</td>'
            )
          else:
            html.append(
                f'<td style="{td}background:{bg} !important;color:{fg} !important;'
                f'text-align:center;font-weight:{fw};">{val_s}</td>'
            )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)


def render_display_detail_html(df, max_visible=15):
  """Bảng 3: sticky Tên NVBH + Mã KH + Tên KH + header; cuộn dọc ~15 dòng."""
  if df is None or df.empty:
    return '<p>Không có dữ liệu chi tiết.</p>'
  cols = [
      'Tên NVBH', 'Mã KH', 'Tên KH', 'Tên Chương Trình TB',
      'Mức ĐK', 'Số Bộ Ảnh Đã Chụp', 'Thứ VT',
  ]
  max_nv = 12
  max_ten = 12
  if 'Tên NVBH' in df.columns:
    for n in df['Tên NVBH'].astype(str):
      max_nv = max(max_nv, len(n))
  if 'Tên KH' in df.columns:
    for n in df['Tên KH'].astype(str):
      max_ten = max(max_ten, min(len(n), 28))
  w_nv = max(120, min(220, max_nv * 9 + 20))
  w_ma = 90
  w_kh = max(120, min(220, max_ten * 8 + 20))
  left_ma = w_nv
  left_kh = w_nv + w_ma

  th_base = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:6px 5px;font-size:11px;'
      'position:sticky;top:0;z-index:5;'
  )
  td = 'border:1px solid #bce2f5 !important;padding:5px 4px;font-size:11px;'
  sticky_nv = f'position:sticky;left:0;z-index:3;min-width:{w_nv}px;'
  sticky_ma = f'position:sticky;left:{left_ma}px;z-index:3;min-width:{w_ma}px;'
  sticky_kh = f'position:sticky;left:{left_kh}px;z-index:3;min-width:{w_kh}px;'
  th_nv = th_base + f'left:0;z-index:6;min-width:{w_nv}px;'
  th_ma = th_base + f'left:{left_ma}px;z-index:6;min-width:{w_ma}px;'
  th_kh = th_base + f'left:{left_kh}px;z-index:6;min-width:{w_kh}px;'

  max_h = 40 + max_visible * 32
  html = [
      f'<div style="overflow:auto;-webkit-overflow-scrolling:touch;margin-top:16px;'
      f'max-height:{max_h}px;">',
      '<h4 style="color:#1a365d;font-weight:800;margin:8px 0 6px 0;">'
      '📋 CHI TIẾT TỪNG KH THEO NHÂN VIÊN</h4>',
      '<table class="custom-kpi-table" style="border-collapse:separate;border-spacing:0;'
      'width:max-content;min-width:100%;font-family:Arial,sans-serif;">',
      '<thead><tr>',
      f'<th style="{th_nv}">Tên NVBH</th>',
      f'<th style="{th_ma}">Mã KH</th>',
      f'<th style="{th_kh}">Tên KH</th>',
  ]
  for c in cols[3:]:
    html.append(f'<th style="{th_base}">{c}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr>')
    for c in cols:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      sticky = ''
      if c == 'Tên NVBH':
        sticky = sticky_nv
      elif c == 'Mã KH':
        sticky = sticky_ma
      elif c == 'Tên KH':
        sticky = sticky_kh
      al = 'left' if c in ('Tên NVBH', 'Tên KH', 'Tên Chương Trình TB', 'Mức ĐK') else 'center'
      html.append(
          f'<td style="{td}{sticky}background:{bg} !important;text-align:{al};'
          f'white-space:nowrap;">{val}</td>'
      )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  return ''.join(html)


def _df_display_export(df, kind='summary'):
  """Chuẩn hoá DataFrame để xuất CSV/Excel — % dạng xx.x%."""
  if df is None or df.empty:
    return df
  out = df.copy()
  for c in out.columns:
    if str(c).startswith('%') or (isinstance(c, str) and '|%' in c):
      out[c] = out[c].apply(
          lambda x: f'{float(x):.1f}%'
          if pd.notna(x) and str(x).replace('.', '').replace('-', '').isdigit()
          or (isinstance(x, (int, float)) and not isinstance(x, bool))
          else (f'{float(str(x).replace("%","")):.1f}%' if pd.notna(x) and '%' in str(x)
                else x)
      )
      # simpler:
  for c in out.columns:
    cs = str(c)
    if cs.startswith('%') or '|%' in cs or cs.endswith('% ĐÃ CHỤP') or '% ĐÃ CHỤP' in cs:
      def _fmt(x):
        if pd.isna(x):
          return ''
        try:
          return f'{float(str(x).replace("%","").strip()):.1f}%'
        except Exception:
          return x
      out[c] = out[c].map(_fmt)
  return out




def build_orders_line_lt3_detail(df_rpt, report_date, filter_nv=None, df_mcp=None):
  """Chi tiết ĐH ngày BC có tổng line (SKU unique) < 3 — chỉ Kênh OFF."""
  empty = pd.DataFrame(columns=[
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'Tổng Line', 'Giá trị ĐH [Doanh Số]', 'Ngày ĐH',
  ])
  if df_rpt is None or df_rpt.empty or 'date' not in df_rpt.columns:
    return empty

  rd = report_date.date() if hasattr(report_date, 'date') else report_date
  d = df_rpt[df_rpt['date'] == rd].copy()
  if d.empty:
    return empty

  # Chỉ Kênh OFF (map MCP L1)
  try:
    ch_l1 = build_mcp_channel_map(df_mcp) if df_mcp is not None else {}
  except Exception:
    ch_l1 = {}
  if ch_l1:
    def _norm_ma(x):
      if pd.isna(x):
        return ''
      s = str(x).strip()
      if s.endswith('.0'):
        s = s[:-2]
      try:
        return str(int(float(s)))
      except Exception:
        return s
    # Chuẩn hoá key map
    ch_l1_n = {_norm_ma(k): v for k, v in ch_l1.items()}
    def _is_off(ma):
      s = _norm_ma(ma)
      ch = str(ch_l1_n.get(s, ch_l1.get(str(ma).strip(), '')) or '').upper()
      return ch != 'ON'  # OFF hoặc không map → giữ; chỉ loại ON
    ma_col0 = find_col(d, ['Mã CH', 'Mã Cửa hàng', 'Outlet Code', 'Outlet_code'])
    if ma_col0:
      d = d[d[ma_col0].map(_is_off)]
      if d.empty:
        return empty

  def _norm(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  ma_dh_col = find_col(d, ['Mã đơn hàng', 'Mã ĐH', 'Order Code', 'Order No'])
  ma_ch_col = find_col(d, ['Mã CH', 'Mã Cửa hàng', 'Outlet Code', 'Outlet_code'])
  nv_col = find_col(d, ['Tên NVBH', 'Tên NV', 'SM Name', 'Salesman'])
  ten_col = find_col(d, ['Tên cửa hàng', 'Tên CH', 'Tên KH', 'Outlet Name', 'Outlet_name'])
  sku_col = find_col(d, ['Mã sản phẩm', 'Mã SP', 'SKU', 'Product Code']) or (
      'Tên sản phẩm' if 'Tên sản phẩm' in d.columns else None
  )
  val_col = find_col(d, ['Thành tiền trước CK', 'Thành tiền trước chiết khấu',
                         'Tổng tiền', 'Doanh số', 'Amount'])
  ngay_col = find_col(d, ['Ngày ĐH', 'Ngày tạo', 'Order Date', 'Created Date'])

  if not ma_dh_col or not sku_col:
    return empty

  d['_dh'] = d[ma_dh_col].astype(str).str.strip()
  d['_sku'] = d[sku_col].astype(str).str.strip()
  lines = d.groupby('_dh')['_sku'].nunique()
  low = set(lines[lines < 3].index.tolist())
  if not low:
    return empty

  d = d[d['_dh'].isin(low)].copy()
  if nv_selected(filter_nv) and nv_col:
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    d = d[d[nv_col].astype(str).str.strip().isin(vals)]
  if d.empty:
    return empty

  rows = []
  for dh, g in d.groupby('_dh', sort=False):
    n_line = int(lines.get(dh, 0))
    nv = str(g[nv_col].iloc[0]).strip() if nv_col else ''
    ma_kh = _norm(g[ma_ch_col].iloc[0]) if ma_ch_col else ''
    ten_kh = str(g[ten_col].iloc[0]).strip() if ten_col else ''
    try:
      ds = float(pd.to_numeric(g[val_col], errors='coerce').sum()) if val_col else 0.0
    except Exception:
      ds = 0.0
    if ngay_col and pd.notna(g[ngay_col].iloc[0]):
      try:
        ngay_str = pd.to_datetime(g[ngay_col].iloc[0], dayfirst=True, errors='coerce')
        ngay_str = ngay_str.strftime('%d/%m/%Y %H:%M') if pd.notna(ngay_str) else str(rd)
      except Exception:
        ngay_str = str(rd)
    else:
      ngay_str = rd.strftime('%d/%m/%Y') if hasattr(rd, 'strftime') else str(rd)
    rows.append({
        'STT': 0,
        'Tên NVBH': nv,
        'Mã KH': ma_kh,
        'Tên KH': ten_kh,
        'Mã ĐH': dh,
        'Tổng Line': n_line,
        'Giá trị ĐH [Doanh Số]': format_number_vn(ds),
        'Ngày ĐH': ngay_str,
    })

  out = pd.DataFrame(rows)
  if out.empty:
    return empty
  out = out.sort_values(['Tên NVBH', 'Mã ĐH']).reset_index(drop=True)
  out['STT'] = range(1, len(out) + 1)
  return out


def build_orders_meat_ge4_detail(df_rpt, report_date, filter_nv=None, df_mcp=None):
  """Chi tiết ĐH ngày BC có tổng line Meat (Processed Meats) >= 4 — chỉ Kênh OFF."""
  empty = pd.DataFrame(columns=[
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'Line Meat', 'Giá trị ĐH [Doanh Số]', 'Ngày ĐH',
  ])
  if df_rpt is None or df_rpt.empty or 'date' not in df_rpt.columns:
    return empty

  rd = report_date.date() if hasattr(report_date, 'date') else report_date
  d = df_rpt[df_rpt['date'] == rd].copy()
  if d.empty:
    return empty

  # Chỉ Kênh OFF (map MCP L1)
  try:
    ch_l1 = build_mcp_channel_map(df_mcp) if df_mcp is not None else {}
  except Exception:
    ch_l1 = {}
  if ch_l1:
    def _norm_ma(x):
      if pd.isna(x):
        return ''
      s = str(x).strip()
      if s.endswith('.0'):
        s = s[:-2]
      try:
        return str(int(float(s)))
      except Exception:
        return s
    # Chuẩn hoá key map
    ch_l1_n = {_norm_ma(k): v for k, v in ch_l1.items()}
    def _is_off(ma):
      s = _norm_ma(ma)
      ch = str(ch_l1_n.get(s, ch_l1.get(str(ma).strip(), '')) or '').upper()
      return ch != 'ON'  # OFF hoặc không map → giữ; chỉ loại ON
    ma_col0 = find_col(d, ['Mã CH', 'Mã Cửa hàng', 'Outlet Code', 'Outlet_code'])
    if ma_col0:
      d = d[d[ma_col0].map(_is_off)]
      if d.empty:
        return empty

  def _norm(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  ma_dh_col = find_col(d, ['Mã đơn hàng', 'Mã ĐH', 'Order Code', 'Order No'])
  ma_ch_col = find_col(d, ['Mã CH', 'Mã Cửa hàng', 'Outlet Code', 'Outlet_code'])
  nv_col = find_col(d, ['Tên NVBH', 'Tên NV', 'SM Name', 'Salesman'])
  ten_col = find_col(d, ['Tên cửa hàng', 'Tên CH', 'Tên KH', 'Outlet Name', 'Outlet_name'])
  sku_col = find_col(d, ['Mã sản phẩm', 'Mã SP', 'SKU', 'Product Code']) or (
      'Tên sản phẩm' if 'Tên sản phẩm' in d.columns else None
  )
  val_col = find_col(d, ['Thành tiền trước CK', 'Thành tiền trước chiết khấu',
                         'Tổng tiền', 'Doanh số', 'Amount'])
  ngay_col = find_col(d, ['Ngày ĐH', 'Ngày tạo', 'Order Date', 'Created Date'])
  sub_col = find_col(d, ['Sub Division', 'SubDivision', 'Phân nhóm', 'Ngành hàng'])

  if not ma_dh_col or not sku_col:
    return empty

  # Lọc dòng Meat
  if 'Tên SP lower' not in d.columns and 'Tên sản phẩm' in d.columns:
    d['Tên SP lower'] = d['Tên sản phẩm'].astype(str).str.lower()
  name = d['Tên SP lower'] if 'Tên SP lower' in d.columns else pd.Series('', index=d.index)
  if sub_col:
    sub = d[sub_col].astype(str)
  else:
    sub = pd.Series('', index=d.index)
  is_meat = sub.str.contains(
      'Processed Meats|Thịt chế biến', case=False, na=False
  ) | name.str.contains(
      'xúc xích|ponnie|cao bồi|hotdog|thịt nguội|ham |pate', na=False
  )
  meat = d[is_meat].copy()
  if meat.empty:
    return empty

  meat['_dh'] = meat[ma_dh_col].astype(str).str.strip()
  meat['_sku'] = meat[sku_col].astype(str).str.strip()
  lines = meat.groupby('_dh')['_sku'].nunique()
  ok = set(lines[lines >= 4].index.tolist())
  if not ok:
    return empty

  # Lấy full order rows (để tính doanh số cả đơn) cho các ĐH đủ điều kiện
  d['_dh'] = d[ma_dh_col].astype(str).str.strip()
  d = d[d['_dh'].isin(ok)].copy()
  if nv_selected(filter_nv) and nv_col:
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    d = d[d[nv_col].astype(str).str.strip().isin(vals)]
  if d.empty:
    return empty

  rows = []
  for dh, g in d.groupby('_dh', sort=False):
    n_meat = int(lines.get(dh, 0))
    # LPPC Total = tổng line (SKU unique) cả đơn
    if sku_col and sku_col in g.columns:
      n_total = int(g[sku_col].astype(str).str.strip().nunique())
    else:
      n_total = int(g['_sku'].nunique()) if '_sku' in g.columns else n_meat
    nv = str(g[nv_col].iloc[0]).strip() if nv_col else ''
    ma_kh = _norm(g[ma_ch_col].iloc[0]) if ma_ch_col else ''
    ten_kh = str(g[ten_col].iloc[0]).strip() if ten_col else ''
    try:
      ds = float(pd.to_numeric(g[val_col], errors='coerce').sum()) if val_col else 0.0
    except Exception:
      ds = 0.0
    if ngay_col and pd.notna(g[ngay_col].iloc[0]):
      try:
        ngay_str = pd.to_datetime(g[ngay_col].iloc[0], dayfirst=True, errors='coerce')
        ngay_str = ngay_str.strftime('%d/%m/%Y %H:%M') if pd.notna(ngay_str) else str(rd)
      except Exception:
        ngay_str = str(rd)
    else:
      ngay_str = rd.strftime('%d/%m/%Y') if hasattr(rd, 'strftime') else str(rd)
    # Chỉ hiển thị khi (LPPC Total - LPPC Meat) < 4 (gồm = 3, 2, 1, 0...)
    if (n_total - n_meat) >= 4:
      continue
    rows.append({
        'STT': 0,
        'Tên NVBH': nv,
        'Mã KH': ma_kh,
        'Tên KH': ten_kh,
        'Mã ĐH': dh,
        'LPPC Meat': n_meat,
        'LPPC Total': n_total,
        'Giá trị ĐH [Doanh Số]': format_number_vn(ds),
        'Ngày ĐH': ngay_str,
    })

  out = pd.DataFrame(rows)
  if out.empty:
    return empty
  out = out.sort_values(['Tên NVBH', 'Mã ĐH']).reset_index(drop=True)
  out['STT'] = range(1, len(out) + 1)
  return out


def _render_order_detail_html(df, title, cols, table_cls='ord-detail-table'):
  """Render bảng chi tiết ĐH — format giống Trái Tuyến / VIP KO ĐH."""
  if df is None or df.empty:
    return ''
  for c in cols:
    if c not in df.columns:
      df[c] = ''
  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:8px 6px;font-size:12px;'
      'white-space:nowrap;'
  )
  td_base = (
      'border:1px solid #bce2f5 !important;padding:6px 5px;font-size:12px;'
      'text-align:center !important;white-space:nowrap;'
  )
  css = (
      '<style>'
      f'.{table_cls}-wrap{{margin-top:20px;width:100%;}}'
      f'.{table_cls}-scroll{{overflow-x:auto;-webkit-overflow-scrolling:touch;width:100%;}}'
      f'.{table_cls}{{border-collapse:collapse;width:100%;min-width:720px;'
      'font-family:Arial,sans-serif;}}'
      f'@media (max-width:768px){{.{table_cls}{{min-width:640px;}}'
      f'.{table_cls} th,.{table_cls} td{{padding:5px 4px !important;font-size:11px !important;}}}}'
      '</style>'
  )
  html = [
      css,
      f'<div class="{table_cls}-wrap">',
      f'<h4 style="color:#1a365d;font-weight:800;margin:8px 0 6px 0;">{title}</h4>',
      f'<div class="{table_cls}-scroll">',
      f'<table class="custom-kpi-table {table_cls}">',
      '<thead><tr>',
  ]
  for c in cols:
    html.append(f'<th style="{th}">{c}</th>')
  html.append('</tr></thead><tbody>')
  for pos, (_, row) in enumerate(df.iterrows()):
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr>')
    for c in cols:
      val = row.get(c, '') if hasattr(row, 'get') else (row[c] if c in getattr(row, 'index', []) else '')
      if pd.isna(val):
        val = ''
      al = 'left' if c in ('Tên NVBH', 'Tên KH') else 'center'
      html.append(
          f'<td style="{td_base}background-color:{bg} !important;'
          f'text-align:{al} !important;">{val}</td>'
      )
    html.append('</tr>')
  html.append('</tbody></table></div></div>')
  return ''.join(html)


def render_orders_line_lt3_html(df):
  cols = [
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'Tổng Line', 'Giá trị ĐH [Doanh Số]', 'Ngày ĐH',
  ]
  return _render_order_detail_html(
      df,
      '📋 CHI TIẾT ĐƠN HÀNG TỔNG LINE &lt; 3',
      cols,
      'ord-lt3',
  )


def render_orders_meat_ge4_html(df):
  cols = [
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'LPPC Meat', 'LPPC Total', 'Giá trị ĐH [Doanh Số]', 'Ngày ĐH',
  ]
  return _render_order_detail_html(
      df,
      '🥩 CHI TIẾT ĐƠN HÀNG MEAT ≥ 4 LINE',
      cols,
      'ord-meat4',
  )


def build_vip_ko_dh_detail(df_visit, df_mcp, report_date, filter_nv=None):
  """Chi tiết CH VIP đã VT trong ngày BC nhưng KHÔNG có đơn hàng."""
  empty = pd.DataFrame(columns=[
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'VIP',
      'Ngày VT thực tế', 'Số Phút Viếng Thăm', 'Trạng thái',
  ])
  if df_visit is None or df_visit.empty:
    return empty

  rd = report_date.date() if hasattr(report_date, 'date') else report_date
  vis = df_visit.copy()

  if 'Ngày VT thực tế' in vis.columns:
    vis['_actual'] = pd.to_datetime(
        vis['Ngày VT thực tế'], dayfirst=True, errors='coerce'
    ).dt.date
  elif '_actual' not in vis.columns:
    return empty

  def _norm(x):
    if pd.isna(x):
      return ''
    s = str(x).strip()
    if s.endswith('.0'):
      s = s[:-2]
    try:
      return str(int(float(s)))
    except Exception:
      return s

  vis['_ma'] = (
      vis['Mã Cửa hàng'].map(_norm) if 'Mã Cửa hàng' in vis.columns else ''
  )
  vis['_nv'] = (
      vis['Tên NVBH'].astype(str).str.strip() if 'Tên NVBH' in vis.columns else ''
  )
  vis['_status'] = (
      vis['Trạng thái'].astype(str).str.strip() if 'Trạng thái' in vis.columns else ''
  )
  vis['_nhom'] = (
      vis['Tên Nhóm CH'].astype(str).str.strip()
      if 'Tên Nhóm CH' in vis.columns else ''
  )
  # Số phút viếng thăm
  _phut_col = None
  for _c in vis.columns:
    if str(_c).strip().lower().replace(' ', '') in (
        'sốphútviếngthăm', 'sophutviengtham', 'sốphútvt', 'sophutvt'
    ) or 'phút' in str(_c).lower() or 'phut' in str(_c).lower().replace('ú', 'u'):
      _phut_col = _c
      break
  if _phut_col:
    vis['_phut'] = pd.to_numeric(vis[_phut_col], errors='coerce')
  else:
    vis['_phut'] = None
  vis['_ten_kh'] = (
      vis['Tên Cửa hàng'].astype(str).str.strip()
      if 'Tên Cửa hàng' in vis.columns
      else (
          vis['Tên CH'].astype(str).str.strip()
          if 'Tên CH' in vis.columns else ''
      )
  )

  # MCP VIP + L1 + tên
  vip_map, l1_map, ten_map = {}, {}, {}
  if df_mcp is not None and not df_mcp.empty:
    c_ma = find_col(df_mcp, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    c_vip = find_col(df_mcp, ['VIP MCH', 'VIP_MCH'])
    c_l1 = find_col(df_mcp, ['L1', 'Channel'])
    c_ten = find_col(df_mcp, ['Outlet_name', 'Outlet Name', 'Tên CH', 'Tên cửa hàng'])
    if c_ma:
      for _, r in df_mcp.iterrows():
        ma = _norm(r[c_ma])
        if not ma:
          continue
        if c_vip and pd.notna(r.get(c_vip)):
          vip_map[ma] = str(r[c_vip]).strip().upper()
        if c_l1 and pd.notna(r.get(c_l1)):
          l1_map[ma] = str(r[c_l1])
        if c_ten and pd.notna(r.get(c_ten)):
          ten_map[ma] = str(r[c_ten]).strip()

  def _is_vip(ma, nhom=''):
    v = vip_map.get(ma, '')
    n = str(nhom or '').strip().upper().replace(' ', '')
    return v in ('VIP3', 'VIP5', 'VIPSI') or n in ('VIP3', 'VIP5', 'VIPSI')

  def _kenh(ma):
    l1 = str(l1_map.get(ma, '')).lower()
    if 'on' in l1 and 'off' not in l1:
      return 'ON'
    return 'OFF'

  # Đã VT trong ngày, không có đơn
  v_day = vis[vis['_actual'] == rd].copy()
  if v_day.empty:
    return empty

  v_day['_co_dh'] = v_day['_status'] == 'Có đơn hàng'
  v_day['_da_vt'] = ~v_day['_status'].isin(['Chờ viếng thăm', 'nan', '', 'None'])
  # VIP KO ĐH: đã VT (hoặc status khác chờ) + không có ĐH + VIP
  rows = []
  seen = set()
  for _, r in v_day.iterrows():
    ma = r.get('_ma', '')
    if not ma or r.get('_co_dh'):
      continue
    # Chỉ lấy CH đã VT (không còn chờ viếng thăm)
    if not r.get('_da_vt'):
      continue
    nhom = r.get('_nhom', '')
    if not _is_vip(ma, nhom):
      continue
    key = (r.get('_nv', ''), ma)
    if key in seen:
      continue
    seen.add(key)
    vip_label = vip_map.get(ma, '') or str(nhom).upper()
    ten = r.get('_ten_kh', '') or ten_map.get(ma, '')
    ngay = r.get('_actual', rd)
    phut = r.get('_phut', '')
    if pd.isna(phut) or phut is None:
      phut_s = ''
    else:
      try:
        phut_s = int(phut) if float(phut) == int(float(phut)) else round(float(phut), 1)
      except Exception:
        phut_s = phut
    rows.append({
        'Tên NVBH': r.get('_nv', ''),
        'Mã KH': ma,
        'Tên KH': ten,
        'VIP': vip_label,
        'Ngày VT thực tế': (
            ngay.strftime('%d/%m/%Y') if hasattr(ngay, 'strftime') else str(ngay)
        ),
        'Số Phút Viếng Thăm': phut_s,
        'Trạng thái': r.get('_status', ''),
    })

  if not rows:
    return empty

  out = pd.DataFrame(rows)
  if filter_nv:
    vals = [
        str(v).strip()
        for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])
        if str(v).strip()
    ]
    if vals:
      out = out[out['Tên NVBH'].isin(vals)]
  if out.empty:
    return empty

  out = out.sort_values(['Tên NVBH', 'Mã KH']).reset_index(drop=True)
  out.insert(0, 'STT', range(1, len(out) + 1))
  return out


def render_vip_ko_dh_html(df):
  """Bảng chi tiết VIP KO ĐH — format giống Trái Tuyến + scale mobile."""
  if df is None or df.empty:
    return ''
  cols = [
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'VIP',
      'Ngày VT thực tế', 'Số Phút Viếng Thăm', 'Trạng thái',
  ]
  for c in cols:
    if c not in df.columns:
      df[c] = ''
  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:8px 6px;font-size:12px;'
      'white-space:nowrap;'
  )
  td_base = (
      'border:1px solid #bce2f5 !important;padding:6px 5px;font-size:12px;'
      'text-align:center !important;white-space:nowrap;'
  )
  # CSS scale trên mobile: font/padding nhỏ hơn, cuộn ngang mượt
  mobile_css = (
      '<style>'
      '.vip-ko-wrap{margin-top:20px;width:100%;}'
      '.vip-ko-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;'
      'width:100%;max-width:100%;}'
      '.vip-ko-table{border-collapse:collapse;width:100%;min-width:720px;'
      'font-family:Arial,sans-serif;}'
      '@media (max-width:768px){'
      '.vip-ko-table{min-width:640px;font-size:11px !important;}'
      '.vip-ko-table th,.vip-ko-table td{padding:5px 4px !important;'
      'font-size:11px !important;}'
      '.vip-ko-title{font-size:14px !important;}'
      '}'
      '@media (max-width:480px){'
      '.vip-ko-table{min-width:560px;font-size:10px !important;}'
      '.vip-ko-table th,.vip-ko-table td{padding:4px 3px !important;'
      'font-size:10px !important;}'
      '.vip-ko-title{font-size:13px !important;}'
      '}'
      '</style>'
  )
  html = [
      mobile_css,
      '<div class="vip-ko-wrap">',
      '<h4 class="vip-ko-title" style="color:#1a365d;font-weight:800;margin:8px 0 6px 0;">'
      '📋 CHI TIẾT KH VIP KO ĐƠN HÀNG</h4>',
      '<div class="vip-ko-scroll">',
      '<table class="custom-kpi-table vip-ko-table">',
      '<thead><tr>',
  ]
  for c in cols:
    html.append(f'<th style="{th}">{c}</th>')
  html.append('</tr></thead><tbody>')
  for pos, (_, row) in enumerate(df.iterrows()):
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr>')
    for c in cols:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      al = 'left' if c in ('Tên NVBH', 'Tên KH') else 'center'
      # VIP: tô đỏ nhạt
      if c == 'VIP' and str(val).strip():
        html.append(
            f'<td style="{td_base}background-color:#fed7d7 !important;'
            f'color:#742a2a !important;font-weight:800;">{val}</td>'
        )
      else:
        html.append(
            f'<td style="{td_base}background-color:{bg} !important;'
            f'text-align:{al} !important;">{val}</td>'
        )
    html.append('</tr>')
  html.append('</tbody></table></div></div>')
  return ''.join(html)


def render_trai_tuyen_html(df):
  """Bảng chi tiết ĐH Trái Tuyến — format giống bảng Hiệu Suất (header xanh đậm, chữ trắng)."""
  if df is None or df.empty:
    return ''
  cols = [
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'Giá trị ĐH [Doanh Số]', 'Ngày ĐH', 'LPPC',
      'Check Lịch VT', 'Check Danh Sách bổ sung',
  ]
  for c in cols:
    if c not in df.columns:
      df[c] = ''

  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:8px 6px;font-size:12px;'
      'white-space:nowrap;'
  )
  td_base = (
      'border:1px solid #bce2f5 !important;padding:6px 5px;font-size:12px;'
      'text-align:center !important;white-space:nowrap;'
  )
  mobile_css = (
      '<style>'
      '.trai-wrap{margin-top:20px;width:100%;}'
      '.trai-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;'
      'width:100%;max-width:100%;}'
      '.trai-table{border-collapse:collapse;width:100%;min-width:860px;'
      'font-family:Arial,sans-serif;}'
      '@media (max-width:768px){'
      '.trai-table{min-width:720px;font-size:11px !important;}'
      '.trai-table th,.trai-table td{padding:5px 4px !important;'
      'font-size:11px !important;}'
      '.trai-title{font-size:14px !important;}'
      '}'
      '@media (max-width:480px){'
      '.trai-table{min-width:640px;font-size:10px !important;}'
      '.trai-table th,.trai-table td{padding:4px 3px !important;'
      'font-size:10px !important;}'
      '.trai-title{font-size:13px !important;}'
      '}'
      '</style>'
  )
  html = [
      mobile_css,
      '<div class="trai-wrap">',
      '<h4 class="trai-title" style="color:#1a365d;font-weight:800;margin:8px 0 6px 0;">'
      '📋 CHI TIẾT ĐƠN HÀNG TRÁI TUYẾN</h4>',
      '<div class="trai-scroll">',
      '<table class="custom-kpi-table trai-table">',
      '<thead><tr>',
  ]
  for c in cols:
    html.append(f'<th style="{th}">{c}</th>')
  html.append('</tr></thead><tbody>')

  n = len(df)
  for pos, (_, row) in enumerate(df.iterrows()):
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr>')
    for c in cols:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      # Check bổ sung: tick xanh đậm
      if c == 'Check Danh Sách bổ sung' and str(val).strip() in ('✓', '✔', '☑'):
        cell = (
            f'<td style="{td_base}background-color:{bg} !important;'
            f'color:#228b22 !important;font-weight:900 !important;'
            f'font-size:16px;">✓</td>'
        )
      else:
        al = 'left' if c in ('Tên NVBH', 'Tên KH', 'Check Lịch VT') else 'center'
        cell = (
            f'<td style="{td_base}background-color:{bg} !important;'
            f'text-align:{al} !important;">{val}</td>'
        )
      html.append(cell)
    html.append('</tr>')

  html.append('</tbody></table></div></div>')
  return ''.join(html)



def build_combo_orders_detail(df_rpt, report_date, filter_nv=None, mcp_df=None):
  """Danh sách đơn hàng Combo theo đúng ngày báo cáo.
  Giữ cùng cấu trúc hiển thị với chi tiết ĐH Trái Tuyến của Báo Cáo Hiệu Suất,
  thay 2 cột cuối thành Loại Hình L1 và Sản Phẩm Khuyến Mãi.
  """
  empty = pd.DataFrame(columns=[
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'Giá trị ĐH [Doanh Số]', 'Ngày ĐH', 'Loại Hình L1',
      'Sản Phẩm Khuyến Mãi',
  ])
  if df_rpt is None or df_rpt.empty or 'date' not in df_rpt.columns:
    return empty

  rd = report_date.date() if hasattr(report_date, 'date') else report_date
  d = df_rpt[df_rpt['date'] == rd].copy()
  if d.empty:
    return empty

  if nv_selected(filter_nv) and 'Tên NVBH' in d.columns:
    vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
    d = d[d['Tên NVBH'].astype(str).str.strip().isin(vals)].copy()
  if d.empty:
    return empty

  # Dùng đúng rule nhận diện Combo đang chạy trong Báo Cáo ĐH Combo.
  combo = tag_combo_orders_t10(d, mcp_df=mcp_df)
  if combo is None or combo.empty:
    return empty

  val_col = find_col(
      combo, ['Thành tiền trước CK', 'Thành tiền trước chiết khấu']
  ) or 'Thành tiền trước CK'
  if val_col in combo.columns:
    combo['_sales'] = pd.to_numeric(combo[val_col], errors='coerce').fillna(0)
  else:
    combo['_sales'] = 0

  if 'Mã đơn hàng' not in combo.columns:
    return empty

  ma_kh_col = find_col(combo, ['Mã CH', 'Mã KH', 'Outlet_code', 'Outlet Code'])
  ten_kh_col = find_col(combo, ['Tên CH', 'Tên khách hàng', 'Tên Cửa hàng'])
  nv_col = find_col(combo, ['Tên NVBH', 'Tên NV', 'SM name', 'Nhân viên'])
  l1_col = find_col(combo, ['L1', 'Channel', 'Loại Hình Kinh Doanh', 'Loại hình kinh doanh'])
  km_col = find_col(combo, ['Hàng KM', 'Hang KM', 'Hàng khuyến mãi'])
  sp_col = find_col(combo, ['Tên sản phẩm', 'Tên SP', 'Sản phẩm'])

  rows = []
  for ma_dh, g in combo.groupby('Mã đơn hàng', sort=False):
    g = g.copy()
    ma_kh = ''
    if ma_kh_col:
      vals_kh = g[ma_kh_col].dropna().astype(str).str.strip()
      if not vals_kh.empty:
        ma_kh = vals_kh.iloc[0]

    ten_kh = ''
    if ten_kh_col:
      vals_ten = g[ten_kh_col].dropna().astype(str).str.strip()
      if not vals_ten.empty:
        ten_kh = vals_ten.iloc[0]

    nv = ''
    if nv_col:
      vals_nv = g[nv_col].dropna().astype(str).str.strip()
      if not vals_nv.empty:
        nv = vals_nv.iloc[0]

    # Ưu tiên L1 thực tế trong RPT (đã map từ Data_MCP); fallback channel ON/OFF.
    l1 = ''
    if l1_col:
      vals_l1 = g[l1_col].dropna().astype(str).str.strip()
      vals_l1 = vals_l1[~vals_l1.str.lower().isin(['', 'nan', 'none'])]
      if not vals_l1.empty:
        l1 = vals_l1.iloc[0]
    if not l1:
      vals_ch = g.get('channel', pd.Series(dtype=object)).dropna().astype(str).str.strip()
      if not vals_ch.empty:
        l1 = vals_ch.iloc[0]

    # Chỉ lấy các dòng Hàng KM để tạo danh sách Sản Phẩm Khuyến Mãi.
    promo_names = []
    if sp_col:
      if km_col:
        km_mask = g[km_col].astype(str).str.strip().str.upper().isin(
            ['Y', 'YES', '1', 'TRUE']
        )
        promo_series = g.loc[km_mask, sp_col]
      else:
        promo_series = g.loc[g['_line_combo'].fillna(False), sp_col]
      for x in promo_series.dropna().astype(str).str.strip().tolist():
        if x and x.lower() not in ('nan', 'none') and x not in promo_names:
          promo_names.append(x)

    ngay_s = ''
    if 'Ngày tạo đơn hàng' in g.columns:
      ngay = pd.to_datetime(g['Ngày tạo đơn hàng'].iloc[0], errors='coerce')
      if pd.notna(ngay):
        ngay_s = ngay.strftime('%d/%m/%Y %H:%M')
    if not ngay_s:
      ngay_s = rd.strftime('%d/%m/%Y') if hasattr(rd, 'strftime') else str(rd)

    rows.append({
        'STT': 0,
        'Tên NVBH': nv,
        'Mã KH': ma_kh,
        'Tên KH': ten_kh,
        'Mã ĐH': str(ma_dh).strip(),
        'Giá trị ĐH [Doanh Số]': int(round(float(g['_sales'].sum()), 0)),
        'Ngày ĐH': ngay_s,
        'Loại Hình L1': l1,
        'Sản Phẩm Khuyến Mãi': ' | '.join(promo_names),
    })

  if not rows:
    return empty

  out = pd.DataFrame(rows).sort_values(
      ['Tên NVBH', 'Mã KH', 'Mã ĐH']
  ).reset_index(drop=True)
  out['STT'] = range(1, len(out) + 1)
  out['Giá trị ĐH [Doanh Số]'] = out['Giá trị ĐH [Doanh Số]'].apply(
      lambda x: f'{int(x):,}'.replace(',', '.') if isinstance(x, (int, float)) else x
  )
  return out







def build_combo_miss_detail(df_rpt, report_date, df_master, channel, filter_nv=None, mcp_df=None):
  """ĐH đạt ĐK chính (OFF≥800k / ON≥300k) nhưng thiếu KM Combo.

  BẮT BUỘC đối chiếu Mã CH với Danh Sách KH được Áp Dụng ĐH Combo
  (file Combo Kênh OFF / Combo Kênh ON trên Github — cột outlet_code).
  """
  empty = pd.DataFrame(columns=[
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'Giá trị ĐH [Doanh Số]', 'Ngày ĐH', 'Loại Hình L1', 'Ghi chú',
  ])
  try:
    if df_rpt is None or df_rpt.empty or 'date' not in df_rpt.columns:
      return empty
    if df_master is None or (hasattr(df_master, 'empty') and df_master.empty):
      return empty

    min_sales = 800000.0 if str(channel).upper() == 'OFF' else 300000.0
    rd = report_date.date() if hasattr(report_date, 'date') else report_date
    month_start = date(rd.year, rd.month, 1)
    # Chuẩn hoá cột date → date thuần để so sánh MTD
    d = df_rpt.copy()
    if 'date' in d.columns:
      _dd = pd.to_datetime(d['date'], errors='coerce')
      d['_d'] = _dd.dt.date
      d = d[(d['_d'] >= month_start) & (d['_d'] <= rd)].copy()
    else:
      d = d.iloc[0:0].copy()
    if d.empty:
      return empty
    if nv_selected(filter_nv) and 'Tên NVBH' in d.columns:
      vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
      d = d[d['Tên NVBH'].astype(str).str.strip().isin(vals)].copy()
    if d.empty:
      return empty

    def _nc(x):
      s = str(x).strip()
      if not s or s.lower() in ('nan', 'none', ''):
        return ''
      if s.endswith('.0'):
        s = s[:-2]
      try:
        # bỏ .0 / scientific
        f = float(s)
        if f == int(f):
          return str(int(f))
        return str(f)
      except Exception:
        return s

    # === DS KH Áp Dụng Combo: outlet_code (cùng build_combo_matrix) ===
    master = df_master.copy()
    master.columns = [str(c).strip() for c in master.columns]
    c_ma_m = None
    # exact names used by matrix
    for cand in ['outlet_code', 'Outlet_code', 'Outlet Code', 'OUTLET_CODE']:
      if cand in master.columns:
        c_ma_m = cand
        break
    if c_ma_m is None:
      c_ma_m = find_col(master, [
          'outlet_code', 'Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH',
          'Customer Code', 'Ship-to', 'Ship To', 'Ship-To',
      ])
    if c_ma_m is None:
      for c in master.columns:
        cl = str(c).lower().replace(' ', '').replace('_', '')
        if 'outlet' in cl or cl in ('mach', 'makh', 'customercode', 'shipto'):
          c_ma_m = c
          break
    if not c_ma_m:
      return empty

    master['_ma'] = master[c_ma_m].map(_nc)
    master = master[master['_ma'] != '']
    master_set = set(master['_ma'].unique())
    if not master_set:
      return empty

    # Optional: filter master by NV if master has Tên NV
    c_nv_m = None
    for cand in ['Tên NV', 'Tên NVBH', 'SM name', 'Nhân viên']:
      if cand in master.columns:
        c_nv_m = cand
        break
    if c_nv_m is None:
      c_nv_m = find_col(master, ['Tên NV', 'Tên NVBH', 'SM name', 'Nhân viên'])
    if nv_selected(filter_nv) and c_nv_m:
      vals = [str(v).strip() for v in (filter_nv if isinstance(filter_nv, list) else [filter_nv])]
      master_nv = master[master[c_nv_m].astype(str).str.strip().isin(vals)]
      if not master_nv.empty:
        master_set = set(master_nv['_ma'].unique())

    ma_col = find_col(d, ['Mã CH', 'Mã KH', 'Outlet_code', 'Outlet Code', 'outlet_code'])
    if not ma_col:
      return empty
    d = d.copy()
    d['_ma'] = d[ma_col].map(_nc)

    # Chỉ giữ ĐH của CH có trong DS KH Áp Dụng Combo
    d = d[d['_ma'].isin(master_set)].copy()
    if d.empty:
      return empty

    # Gắn is_combo trên toàn bộ ĐH (không lọc chỉ combo)
    tagged = tag_all_orders_with_combo_flag(d, mcp_df=mcp_df)
    if tagged is None or tagged.empty:
      return empty
    if 'Mã đơn hàng' not in tagged.columns:
      return empty

    val_col = find_col(tagged, [
        'Thành tiền trước CK', 'Thành tiền trước chiết khấu',
        'Tổng tiền', 'Giá trị sau CK',
    ])
    tagged['_sales'] = pd.to_numeric(tagged[val_col], errors='coerce').fillna(0) if val_col else 0
    if '_ma' not in tagged.columns:
      tagged['_ma'] = tagged[ma_col].map(_nc) if ma_col in tagged.columns else ''
    # double-check still in master
    tagged = tagged[tagged['_ma'].isin(master_set)].copy()
    if tagged.empty:
      return empty

    order_sales = tagged.groupby(tagged['Mã đơn hàng'].astype(str))['_sales'].sum()
    order_combo = tagged.groupby(tagged['Mã đơn hàng'].astype(str))['is_combo'].any()
    order_ma = tagged.groupby(tagged['Mã đơn hàng'].astype(str))['_ma'].first()
    if '_d' in tagged.columns:
      order_date = tagged.groupby(tagged['Mã đơn hàng'].astype(str))['_d'].first()
    elif 'date' in tagged.columns:
      order_date = tagged.groupby(tagged['Mã đơn hàng'].astype(str))['date'].first()
    else:
      order_date = pd.Series(dtype=object)

    ten_kh_col = find_col(tagged, ['Tên CH', 'Tên khách hàng', 'Tên Cửa hàng'])
    nv_col = find_col(tagged, ['Tên NVBH', 'Tên NV', 'SM name', 'Nhân viên'])
    l1_col = find_col(tagged, ['L1', 'Channel', 'Loại Hình Kinh Doanh'])

    rows = []
    for ma_dh, sales in order_sales.items():
      if float(sales) < min_sales:
        continue
      if bool(order_combo.get(ma_dh, False)):
        continue
      g = tagged[tagged['Mã đơn hàng'].astype(str) == str(ma_dh)]
      ma_kh = str(order_ma.get(ma_dh, '') or '')
      if ma_kh not in master_set:
        continue
      ten_kh, nv, l1 = '', '', channel
      if ten_kh_col is not None and not g.empty:
        vv = g[ten_kh_col].dropna().astype(str).str.strip()
        if not vv.empty:
          ten_kh = vv.iloc[0]
      if nv_col is not None and not g.empty:
        vv = g[nv_col].dropna().astype(str).str.strip()
        if not vv.empty:
          nv = vv.iloc[0]
      if l1_col is not None and not g.empty:
        vv = g[l1_col].dropna().astype(str).str.strip()
        if not vv.empty:
          l1 = vv.iloc[0]
      # Ngày ĐH thực tế của đơn
      od = order_date.get(ma_dh, rd) if len(order_date) else rd
      try:
        if hasattr(od, 'strftime'):
          ngay_str = od.strftime('%d/%m/%Y')
        else:
          od2 = pd.to_datetime(od, errors='coerce')
          ngay_str = od2.strftime('%d/%m/%Y') if pd.notna(od2) else str(od)
      except Exception:
        ngay_str = str(od)
      rows.append({
          'STT': 0,
          'Tên NVBH': nv,
          'Mã KH': ma_kh,
          'Tên KH': ten_kh,
          'Mã ĐH': str(ma_dh),
          'Giá trị ĐH [Doanh Số]': f'{float(sales):,.0f}'.replace(',', '.'),
          'Ngày ĐH': ngay_str,
          'Loại Hình L1': l1,
          'Ghi chú': f'Có trong DS Combo {channel} · Đạt ĐK chính (≥{min_sales:,.0f}đ) · Thiếu ĐK phụ/KM'.replace(',', '.'),
          '_sales': float(sales),
          '_date': od if hasattr(od, 'year') else rd,
      })
    if not rows:
      return empty
    out = pd.DataFrame(rows).sort_values(['Tên NVBH', 'Mã KH']).reset_index(drop=True)
    out['STT'] = range(1, len(out) + 1)
    return out
  except Exception as e:
    try:
      import streamlit as _st
      _st.caption(f'(Combo miss {channel}: {type(e).__name__}: {e})')
    except Exception:
      pass
    return empty



def build_combo_miss_summary(df_miss_off, df_miss_on):
  """Tổng hợp theo NV: số ĐH miss Combo OFF/ON + doanh số."""
  cols = [
      'STT', 'Tên NVBH',
      'Số ĐH miss OFF', 'DS miss OFF',
      'Số ĐH miss ON', 'DS miss ON',
      'Tổng ĐH miss', 'Tổng DS miss',
  ]
  empty = pd.DataFrame(columns=cols)

  def _agg(df):
    if df is None or df.empty or 'Tên NVBH' not in df.columns:
      return {}
    d = df.copy()
    if '_sales' not in d.columns:
      d['_sales'] = (
          d['Giá trị ĐH [Doanh Số]'].astype(str)
          .str.replace('.', '', regex=False)
          .str.replace(',', '', regex=False)
      )
      d['_sales'] = pd.to_numeric(d['_sales'], errors='coerce').fillna(0)
    g = d.groupby('Tên NVBH').agg(n=('Mã ĐH', 'nunique'), ds=('_sales', 'sum'))
    return g.to_dict('index')

  off = _agg(df_miss_off)
  on = _agg(df_miss_on)
  nvs = sorted(set(list(off.keys()) + list(on.keys())))
  if not nvs:
    return empty
  rows = []
  for nv in nvs:
    n_off = int(off.get(nv, {}).get('n', 0) or 0)
    ds_off = float(off.get(nv, {}).get('ds', 0) or 0)
    n_on = int(on.get(nv, {}).get('n', 0) or 0)
    ds_on = float(on.get(nv, {}).get('ds', 0) or 0)
    rows.append({
        'STT': 0,
        'Tên NVBH': nv,
        'Số ĐH miss OFF': n_off,
        'DS miss OFF': f'{ds_off:,.0f}'.replace(',', '.'),
        'Số ĐH miss ON': n_on,
        'DS miss ON': f'{ds_on:,.0f}'.replace(',', '.'),
        'Tổng ĐH miss': n_off + n_on,
        'Tổng DS miss': f'{ds_off + ds_on:,.0f}'.replace(',', '.'),
    })
  out = pd.DataFrame(rows)
  out['STT'] = range(1, len(out) + 1)
  # total
  tot_off = int(out['Số ĐH miss OFF'].sum())
  tot_on = int(out['Số ĐH miss ON'].sum())
  ds_off = sum(float(str(x).replace('.', '')) for x in out['DS miss OFF'])
  ds_on = sum(float(str(x).replace('.', '')) for x in out['DS miss ON'])
  out = pd.concat([out, pd.DataFrame([{
      'STT': '',
      'Tên NVBH': 'TỔNG CỘNG',
      'Số ĐH miss OFF': tot_off,
      'DS miss OFF': f'{ds_off:,.0f}'.replace(',', '.'),
      'Số ĐH miss ON': tot_on,
      'DS miss ON': f'{ds_on:,.0f}'.replace(',', '.'),
      'Tổng ĐH miss': tot_off + tot_on,
      'Tổng DS miss': f'{ds_off + ds_on:,.0f}'.replace(',', '.'),
  }])], ignore_index=True)
  return out



def render_combo_orders_html(df):
  """Bảng chi tiết ĐH Combo — format giống Chi Tiết ĐH Trái Tuyến."""
  if df is None or df.empty:
    return ''
  df = df.drop(columns=['Mã NVBH'], errors='ignore')
  cols = [
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'Giá trị ĐH [Doanh Số]', 'Ngày ĐH', 'Loại Hình L1',
      'Sản Phẩm Khuyến Mãi',
  ]
  if 'Ghi chú' in df.columns:
    cols = [c for c in cols if c != 'Sản Phẩm Khuyến Mãi'] + ['Ghi chú']
  for c in cols:
    if c not in df.columns:
      df[c] = ''
  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:8px 6px;font-size:12px;'
      'white-space:nowrap;'
  )
  td_base = (
      'border:1px solid #bce2f5 !important;padding:6px 5px;font-size:12px;'
      'text-align:center !important;white-space:nowrap;'
  )
  html = [
      '<div style="margin-top:12px;">',
      '<h4 style="color:#1a365d;font-weight:800;margin:8px 0 6px 0;">'
      '📋 CHI TIẾT ĐƠN HÀNG COMBO</h4>',
      '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">',
      '<table class="custom-kpi-table" style="border-collapse:collapse;width:100%;'
      'min-width:900px;font-family:Arial,sans-serif;">',
      '<thead><tr>',
  ]
  for c in cols:
    html.append(f'<th style="{th}">{c}</th>')
  html.append('</tr></thead><tbody>')
  for pos, (_, row) in enumerate(df.iterrows()):
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr>')
    for c in cols:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      al = 'left' if c in ('Tên NVBH', 'Tên KH', 'Sản Phẩm Khuyến Mãi') else 'center'
      html.append(
          f'<td style="{td_base}background-color:{bg} !important;'
          f'text-align:{al} !important;">{val}</td>'
      )
    html.append('</tr>')
  html.append('</tbody></table></div></div>')
  return ''.join(html)




def render_combo_miss_table(df, title, key_prefix):
  """Bảng chi tiết miss Combo: max 25 dòng cuộn dọc, sticky STT + Tên NVBH, toolbar CSV/Full."""
  if df is None or df.empty:
    return
  df = df.drop(columns=['Mã NVBH', '_sales', '_date'], errors='ignore').copy()
  cols = [
      'STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'Mã ĐH',
      'Giá trị ĐH [Doanh Số]', 'Ngày ĐH', 'Loại Hình L1', 'Ghi chú',
  ]
  for c in cols:
    if c not in df.columns:
      df[c] = ''
  df = df[[c for c in cols if c in df.columns]]

  t1, t2, t3 = st.columns([2.2, 1.1, 1])
  with t1:
    st.markdown(
        f'<p style="font-weight:800;color:#1a365d;margin:8px 0 4px 0;font-size:14px;">'
        f'📋 {title}</p>',
        unsafe_allow_html=True,
    )
  with t2:
    show_full = st.checkbox('🔍 Xem full bảng', key=f'{key_prefix}_full', value=False)
  with t3:
    csv_bytes = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        '⬇️ Tải CSV',
        data=csv_bytes,
        file_name=f'{key_prefix}.csv',
        mime='text/csv',
        key=f'{key_prefix}_csv',
    )

  w_stt, w_nv = 48, 160
  max_h = 'none' if show_full else '920px'
  th = (
      'background-color:#1a365d !important;color:#ffffff !important;'
      'font-weight:800 !important;text-align:center !important;'
      'border:1px solid #2b6cb0 !important;padding:8px 6px;font-size:12px;'
      'white-space:nowrap;'
  )
  th_sticky = th + 'position:sticky;top:0;z-index:5;'
  td_base = (
      'border:1px solid #bce2f5 !important;padding:6px 5px;font-size:12px;'
      'text-align:center !important;white-space:nowrap;'
  )

  html = [
      f'<div style="overflow:auto;max-height:{max_h};-webkit-overflow-scrolling:touch;'
      f'border:1px solid #bee3f8;border-radius:6px;">',
      '<table class="custom-kpi-table" style="border-collapse:collapse;width:100%;'
      'min-width:980px;font-family:Arial,sans-serif;">',
      '<thead><tr>',
  ]
  for c in df.columns:
    if c == 'STT':
      html.append(
          f'<th style="{th_sticky}left:0;z-index:7;min-width:{w_stt}px;'
          f'box-shadow:2px 0 4px rgba(0,0,0,.08);">{c}</th>'
      )
    elif c == 'Tên NVBH':
      html.append(
          f'<th style="{th_sticky}left:{w_stt}px;z-index:7;min-width:{w_nv}px;'
          f'box-shadow:2px 0 4px rgba(0,0,0,.08);">{c}</th>'
      )
    else:
      html.append(f'<th style="{th_sticky}">{c}</th>')
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df.iterrows()):
    bg = '#e6f4fc' if pos % 2 == 0 else '#ffffff'
    html.append('<tr>')
    for c in df.columns:
      val = row.get(c, '')
      if pd.isna(val):
        val = ''
      al = 'left' if c in ('Tên NVBH', 'Tên KH', 'Ghi chú') else 'center'
      if c == 'STT':
        html.append(
            f'<td style="{td_base}background-color:{bg} !important;text-align:{al};'
            f'position:sticky;left:0;z-index:3;min-width:{w_stt}px;'
            f'box-shadow:2px 0 4px rgba(0,0,0,.06);">{val}</td>'
        )
      elif c == 'Tên NVBH':
        html.append(
            f'<td style="{td_base}background-color:{bg} !important;text-align:left;'
            f'position:sticky;left:{w_stt}px;z-index:3;min-width:{w_nv}px;'
            f'box-shadow:2px 0 4px rgba(0,0,0,.06);font-weight:600;">{val}</td>'
        )
      else:
        html.append(
            f'<td style="{td_base}background-color:{bg} !important;text-align:{al};">{val}</td>'
        )
    html.append('</tr>')
  html.append('</tbody></table></div>')
  if not show_full and len(df) > 25:
    html.append(
        f'<p style="font-size:11px;color:#718096;margin:4px 0 0 0;">'
        f'Cuộn dọc (~25 dòng khung nhìn) · Tổng {len(df):,} dòng · '
        f'Bật "Xem full bảng" hoặc Tải CSV để xem hết.</p>'
    )
  st.markdown(''.join(html), unsafe_allow_html=True)



def build_performance_comments(df):
  """Nhận xét 5 chỉ số: SO, VT KO ĐH, ASO Xanh, ASO Vàng, Trái tuyến & VIP."""
  if df is None or df.empty:
    return ''
  d = df.copy()
  mask_tot = d['STT'].astype(str).str.strip().isin(['-', 'TOTAL', ''])
  if 'Tên NVBH' in d.columns:
    mask_tot = mask_tot | d['Tên NVBH'].astype(str).str.upper().str.contains(
        'TỔNG|TOTAL', na=False
    )
  d = d[~mask_tot].copy()
  if d.empty:
    return ''

  for col in ['_delta_so', '_delta_x', '_delta_v', '_n_trai', '_n_vip_ko',
              '_pct_vt_dh', '_pct_so', '_pct_x', '_pct_v']:
    if col not in d.columns:
      d[col] = 0
    d[col] = pd.to_numeric(d[col], errors='coerce').fillna(0)

  d['_pct_ko_dh'] = (100.0 - d['_pct_vt_dh']).clip(lower=0)

  def _top3(col, fmt='pct', higher_better=True):
    asc = not higher_better
    top = d.sort_values(col, ascending=asc).head(3)
    bot = d.sort_values(col, ascending=not asc).head(3)

    def _f(r):
      v = r[col]
      if fmt == 'pct':
        return f"{r['Tên NVBH']} ({v:.1f}%)"
      if fmt == 'money':
        return f"{r['Tên NVBH']} ({int(v):+,}đ)".replace(',', '.')
      if fmt == 'int':
        return f"{r['Tên NVBH']} ({int(v)})"
      return f"{r['Tên NVBH']} ({v})"

    return (
        ', '.join(_f(r) for _, r in top.iterrows()) or 'Không có',
        ', '.join(_f(r) for _, r in bot.iterrows()) or 'Không có',
    )

  lines = []
  lines.append('<div class="note-box" style="margin-top:14px;">')
  lines.append('<b>📝 NHẬN XÉT HIỆU SUẤT BÁN HÀNG</b><br/><br/>')

  # 1. Doanh Số
  lines.append('<b style="color:#034ea2;">1. Doanh Số</b><br/>')
  up = d[d['_delta_so'] > 0].sort_values('_delta_so', ascending=False).head(3)
  down = d[d['_delta_so'] < 0].sort_values('_delta_so', ascending=True).head(3)
  up_s = ', '.join(
      f"{r['Tên NVBH']} ({int(r['_delta_so']):+,}đ)".replace(',', '.')
      for _, r in up.iterrows()
  ) or 'Không có'
  down_s = ', '.join(
      f"{r['Tên NVBH']} ({int(r['_delta_so']):+,}đ)".replace(',', '.')
      for _, r in down.iterrows()
  ) or 'Không có'
  t3, b3 = _top3('_pct_so', fmt='pct', higher_better=True)
  lines.append(f"• <b>Top 3 tăng SO vs giữa ngày:</b> {up_s}<br/>")
  lines.append(f"• <b>Bottom 3 giảm SO vs giữa ngày:</b> {down_s}<br/>")
  lines.append(f"• <b>Top 3 % TH SO / CT ngày:</b> {t3}<br/>")
  lines.append(f"• <b>Bottom 3 % TH SO / CT ngày:</b> {b3}<br/>")

  # 2. Tỷ lệ VT không có ĐH
  lines.append('<b style="color:#034ea2;">2. Tỷ lệ VT không có ĐH</b><br/>')
  t3, b3 = _top3('_pct_ko_dh', fmt='pct', higher_better=False)
  # higher_better=False → top = lowest KO ĐH (tốt), bot = highest KO ĐH (xấu)
  lines.append(f"• <b>Top 3 tỷ lệ VT KO ĐH thấp nhất (tốt):</b> {t3}<br/>")
  lines.append(f"• <b>Bottom 3 tỷ lệ VT KO ĐH cao nhất:</b> {b3}<br/>")

  # 3. ASO Trận Xanh
  lines.append('<b style="color:#034ea2;">3. ASO Trận Xanh</b><br/>')
  t3, b3 = _top3('_pct_x', fmt='pct', higher_better=True)
  lines.append(f"• <b>Top 3 % TH ASO Xanh:</b> {t3}<br/>")
  lines.append(f"• <b>Bottom 3 % TH ASO Xanh:</b> {b3}<br/>")
  upx = d[d['_delta_x'] > 0].sort_values('_delta_x', ascending=False).head(3)
  upx_s = ', '.join(
      f"{r['Tên NVBH']} (+{int(r['_delta_x'])})" for _, r in upx.iterrows()
  ) or 'Không có'
  lines.append(f"• <b>Top 3 tăng ASO Xanh vs giữa ngày:</b> {upx_s}<br/>")

  # 4. ASO Trận Vàng
  lines.append('<b style="color:#034ea2;">4. ASO Trận Vàng</b><br/>')
  t3, b3 = _top3('_pct_v', fmt='pct', higher_better=True)
  lines.append(f"• <b>Top 3 % TH ASO Vàng:</b> {t3}<br/>")
  lines.append(f"• <b>Bottom 3 % TH ASO Vàng:</b> {b3}<br/>")
  upv = d[d['_delta_v'] > 0].sort_values('_delta_v', ascending=False).head(3)
  upv_s = ', '.join(
      f"{r['Tên NVBH']} (+{int(r['_delta_v'])})" for _, r in upv.iterrows()
  ) or 'Không có'
  lines.append(f"• <b>Top 3 tăng ASO Vàng vs giữa ngày:</b> {upv_s}<br/>")

  # 5. Trái tuyến & VIP KO ĐH
  lines.append('<b style="color:#034ea2;">5. Trái Tuyến & VIP KO ĐH</b><br/>')
  trai = d[d['_n_trai'] > 0].sort_values('_n_trai', ascending=False)
  if trai.empty:
    lines.append('• <b>Bán trái tuyến:</b> Không có<br/>')
  else:
    names = [f"{r['Tên NVBH']} ({int(r['_n_trai'])} CH)" for _, r in trai.iterrows()]
    lines.append(f"• <b>Bán trái tuyến:</b> {', '.join(names)}<br/>")
  vip = d[d['_n_vip_ko'] > 0].sort_values('_n_vip_ko', ascending=False)
  if vip.empty:
    lines.append('• <b>KH VIP không mua hàng:</b> Không có<br/>')
  else:
    names = [f"{r['Tên NVBH']} ({int(r['_n_vip_ko'])} VIP)" for _, r in vip.iterrows()]
    lines.append(f"• <b>KH VIP không mua hàng:</b> {', '.join(names)}<br/>")

  # 6. Kỷ Luật TB: có PER nhưng hôm nay không chụp hình
  lines.append(
      '<b style="color:#034ea2;">6. Kỷ Luật TB — Có CH TB PER nhưng hôm nay không chụp hình</b><br/>'
  )
  c_per = 'Số CH TB PER' if 'Số CH TB PER' in d.columns else None
  c_chup = 'Chụp hình bởi ĐDKD' if 'Chụp hình bởi ĐDKD' in d.columns else None
  if c_per and c_chup:
    d['_per'] = pd.to_numeric(d[c_per], errors='coerce').fillna(0)
    d['_chup'] = pd.to_numeric(d[c_chup], errors='coerce').fillna(0)
    # Có PER > 0 và Chụp = 0
    miss = d[(d['_per'] > 0) & (d['_chup'] <= 0)].sort_values('_per', ascending=False)
    # Có PER nhưng chụp < PER (thiếu)
    gap = d[(d['_per'] > 0) & (d['_chup'] < d['_per'])].copy()
    gap['_thieu'] = gap['_per'] - gap['_chup']
    gap = gap.sort_values('_thieu', ascending=False)
    if miss.empty:
      lines.append(
          '• <b>NV có CH TB PER nhưng 0 chụp hình hôm nay:</b> Không có<br/>'
      )
    else:
      names = [
          f"{r['Tên NVBH']} (PER {int(r['_per'])}, chụp 0)"
          for _, r in miss.iterrows()
      ]
      lines.append(
          f"• <b>NV có CH TB PER nhưng 0 chụp hình hôm nay:</b> {', '.join(names)}<br/>"
      )
    if not gap.empty:
      names = [
          f"{r['Tên NVBH']} (PER {int(r['_per'])}, chụp {int(r['_chup'])}, thiếu {int(r['_thieu'])})"
          for _, r in gap.head(5).iterrows()
      ]
      lines.append(
          f"• <b>NV còn thiếu chụp so với PER (Top 5):</b> {', '.join(names)}<br/>"
      )
  else:
    lines.append('• Không có dữ liệu Kỷ Luật TB<br/>')

  lines.append('</div>')
  return ''.join(lines)





def _fmt_tr(n):
  try:
    n = float(n or 0)
  except Exception:
    return '0'
  if abs(n) >= 1_000_000:
    s = f'{n/1_000_000:.1f}'.replace('.', ',')
    return f'{s} tr'
  if abs(n) >= 1_000:
    return f'{int(round(n/1000))}k'
  return f'{int(round(n))}'


def _pct_color(pct, timegone=None):
  try:
    p = float(str(pct).replace('%', '').replace(',', '.'))
  except Exception:
    return '#e53e3e'
  if timegone is not None:
    try:
      tg = float(timegone)
    except Exception:
      tg = 0
    if p + 5 < tg:
      return '#e53e3e'
    if p >= tg + 5:
      return '#805ad5'
    return '#38a169'
  if p >= 100:
    return '#38a169'
  if p >= 70:
    return '#d69e2e'
  return '#e53e3e'


def render_hs_daily_metric_cards(df_perf, report_date, lppc_moc=4.3, aso_off=None, aso_on=None):
  """Bảng 1: Metric card KPI theo ngày — 2 hàng × 5 card, responsive mobile."""
  if df_perf is None or df_perf.empty:
    return ''
  tot = df_perf.iloc[-1]

  def g(col, default=0):
    try:
      v = tot.get(col, default)
      if pd.isna(v):
        return default
      s = str(v).replace('%', '').replace(',', '.')
      return float(s)
    except Exception:
      return default

  th_so, ct_so = g('TH SO'), g('CT Ngày SO')
  pct_so = (th_so / ct_so * 100) if ct_so else 0
  pc_off = g('PC OFF')
  plan_off = g('Đã VT OFF') or g('Plan VT OFF')
  pct_pc_off = (pc_off / plan_off * 100) if plan_off else 0
  pc_on = g('PC ON')
  plan_on = g('Plan VT ON') or g('Đã VT ON')
  pct_pc_on = (pc_on / plan_on * 100) if plan_on else 0
  lppc = g('LPPC OFF')
  th_x, ct_x = g('TH Xanh'), g('CT Xanh') or 5
  th_v, ct_v = g('TH Vàng'), g('CT Vàng') or 3
  th_co, ct_co = g('TH Combo OFF'), g('CT Combo OFF') or 5
  th_cn, ct_cn = g('TH Combo ON'), g('CT Combo ON') or 3

  # ASO ALL OFF/ON — TH ngày; CT ngày = MCP tháng / số ngày làm việc
  ao = aso_off or {'th': 0, 'mtd': 0, 'ct': 0, 'ct_day': 0}
  an = aso_on or {'th': 0, 'mtd': 0, 'ct': 0, 'ct_day': 0}
  ao_th = int(ao.get('th', 0) or 0)
  an_th = int(an.get('th', 0) or 0)
  ao_mtd = int(ao.get('mtd', 0) or 0)
  an_mtd = int(an.get('mtd', 0) or 0)
  ao_ct = int(ao.get('ct_day', 0) or ao.get('ct', 0) or 0)
  an_ct = int(an.get('ct_day', 0) or an.get('ct', 0) or 0)

  # 10 cards — format TH/CT/%TH (ASO ALL: TH/MTD/CT/%TH)
  pct_lppc = (lppc / lppc_moc * 100) if lppc_moc else 0
  pct_x = (th_x / ct_x * 100) if ct_x else 0
  pct_v = (th_v / ct_v * 100) if ct_v else 0
  pct_co = (th_co / ct_co * 100) if ct_co else 0
  pct_cn = (th_cn / ct_cn * 100) if ct_cn else 0
  # ASO ALL: % = MTD/CT
  pct_ao = (ao_mtd / ao_ct * 100) if ao_ct else 0
  pct_an = (an_mtd / an_ct * 100) if an_ct else 0

  def _fmt_trieu(n):
    """Chỉ số triệu, không gắn chữ 'tr' (đơn vị nằm ở tiêu đề)."""
    try:
      n = float(n or 0) / 1_000_000.0
      return f'{n:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    except Exception:
      return '0'

  cards = [
    (
      'DOANH SỐ NGÀY (Triệu đồng)',
      f'{_fmt_trieu(th_so)}/{_fmt_trieu(ct_so)}/{pct_so:.0f}%',
      'TH/CT/%TH',
      '#e53e3e',
    ),
    (
      'PC BT / PC OFF',
      f'{int(pc_off)}/{int(plan_off)}/{pct_pc_off:.0f}%',
      'TH/CT/%TH',
      '#3182ce',
    ),
    (
      'PC ON',
      f'{int(pc_on)}/{int(plan_on)}/{pct_pc_on:.0f}%',
      'TH/CT/%TH',
      '#dd6b20',
    ),
    (
      'LPPC OFF',
      f'{lppc:.2f}'.replace('.', ',') + f'/{str(lppc_moc).replace(".", ",")}/{pct_lppc:.0f}%',
      'TH/CT/%TH',
      '#38a169',
    ),
    (
      'ASO ALL OFF',
      f'{ao_th}/{ao_mtd}/{ao_ct}/{pct_ao:.0f}%',
      'TH ngày/MTD/CT/%MTD',
      '#805ad5',
    ),
    (
      'ASO ALL ON',
      f'{an_th}/{an_mtd}/{an_ct}/{pct_an:.0f}%',
      'TH ngày/MTD/CT/%MTD',
      '#d53f8c',
    ),
    (
      'ASO TRẬN XANH',
      f'{int(th_x)}/{int(ct_x)}/{pct_x:.0f}%',
      'TH/CT/%TH',
      '#319795',
    ),
    (
      'ASO TRẬN VÀNG',
      f'{int(th_v)}/{int(ct_v)}/{pct_v:.0f}%',
      'TH/CT/%TH',
      '#d69e2e',
    ),
    (
      'COMBO OFF',
      f'{int(th_co)}/{int(ct_co)}/{pct_co:.0f}%',
      'TH/CT/%TH',
      '#2b6cb0',
    ),
    (
      'COMBO ON',
      f'{int(th_cn)}/{int(ct_cn)}/{pct_cn:.0f}%',
      'TH/CT/%TH',
      '#c05621',
    ),
  ]

  wd = report_date.strftime('%d/%m') if hasattr(report_date, 'strftime') else str(report_date)
  try:
    thu_map = {0: 'Thứ Hai', 1: 'Thứ Ba', 2: 'Thứ Tư', 3: 'Thứ Năm', 4: 'Thứ Sáu', 5: 'Thứ Bảy', 6: 'Chủ Nhật'}
    thu = thu_map.get(report_date.weekday(), '')
  except Exception:
    thu = ''

  html = [
    '<style>'
    '.hs-day-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;}'
    '@media(max-width:900px){.hs-day-grid{grid-template-columns:repeat(2,1fr)!important;}}'
    '@media(max-width:480px){.hs-day-grid{grid-template-columns:1fr!important;}}'
    '.hs-day-card{background:#fff;border-radius:12px;padding:12px 14px;'
    'box-shadow:0 1px 4px rgba(0,0,0,.08);border-top:3px solid #cbd5e0;}'
    '.hs-day-card .t{font-size:11px;font-weight:700;color:#718096;letter-spacing:.3px;}'
    '.hs-day-card .m{font-size:20px;font-weight:800;color:#1a202c;margin:4px 0;}'
    '.hs-day-card .s{font-size:12px;color:#4a5568;}'
    '</style>',
    f'<div style="margin:18px 0 8px 0;">'
    f'<div style="font-size:16px;font-weight:800;color:#1a365d;margin-bottom:10px;">'
    f'Kết quả ngày {wd} '
    f'<span style="background:#ebf8ff;color:#2b6cb0;font-size:12px;padding:2px 8px;'
    f'border-radius:12px;margin-left:6px;">{thu}</span></div>'
    f'<div class="hs-day-grid">'
  ]
  for title, main, sub, color in cards:
    html.append(
      f'<div class="hs-day-card" style="border-top-color:{color};">'
      f'<div class="t" style="color:{color};">{title}</div>'
      f'<div class="m">{main}</div>'
      f'<div class="s">{sub}</div></div>'
    )
  html.append('</div></div>')
  return ''.join(html)


def render_hs_monthly_kpi_table(
    rows, timegone, combo_off=None, combo_on=None, mbs_cat=None, mbs_brand=None, report_date=None
):
  """Bảng 2: Lũy kế tháng — format giống Trưng Bày + card Combo/MBS có màu."""
  try:
    tg = float(timegone or 0)
  except Exception:
    tg = 0.0
  label = 'Lũy kế tháng'
  if report_date is not None:
    try:
      label = f'Lũy kế tháng {report_date.month} đến {report_date.strftime("%d/%m")}'
    except Exception:
      pass

  # Palette tương phản cho từng hàng KPI
  _BAR = ['#e53e3e', '#3182ce', '#38a169', '#805ad5', '#dd6b20', '#d53f8c', '#319795', '#d69e2e', '#2b6cb0', '#c05621']

  html = [
    f'<div style="margin:20px 0 8px 0;">'
    f'<div style="font-size:16px;font-weight:800;color:#1a365d;margin-bottom:10px;">{label}</div>'
    f'<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">'
    f'<table class="custom-kpi-table" style="min-width:640px;">'
    f'<thead><tr>'
    f'<th>KPI</th><th>THỰC ĐẠT</th><th>TARGET THÁNG</th><th>% ĐẠT</th>'
    f'<th style="min-width:160px;">TIẾN ĐỘ {tg:.1f}%</th>'
    f'</tr></thead><tbody>'
  ]

  for i, r in enumerate(rows):
    name = r.get('name', '')
    th = r.get('th', 0)
    ct = r.get('ct', 0)
    pct = r.get('pct', 0)
    fmt = r.get('fmt', 'num')
    if fmt == 'money':
      th_s, ct_s = _fmt_tr(th), _fmt_tr(ct)
    elif fmt == 'float':
      th_s = f'{float(th):.2f}'.replace('.', ',')
      ct_s = f'{float(ct):.1f}'.replace('.', ',')
    else:
      th_s, ct_s = f'{int(round(float(th)))}', f'{int(round(float(ct)))}'
    color = _pct_color(pct, tg)
    bar_color = _BAR[i % len(_BAR)]
    bar_w = max(0, min(100, float(pct)))
    tg_pos = max(0, min(100, tg))
    bg = '#f0f7fc' if i % 2 == 0 else '#ffffff'
    html.append(
      f'<tr style="background:{bg};">'
      f'<td style="text-align:left;font-weight:600;padding-left:10px;">{name}</td>'
      f'<td style="text-align:center;font-weight:700;">{th_s}</td>'
      f'<td style="text-align:center;font-weight:800;">{ct_s}</td>'
      f'<td style="text-align:center;font-weight:800;color:{color};">{pct:.1f}%</td>'
      f'<td style="padding:8px 12px;">'
      f'<div style="position:relative;height:12px;background:#e2e8f0;border-radius:6px;">'
      f'<div style="height:100%;width:{bar_w}%;background:{bar_color};border-radius:6px;"></div>'
      f'<div style="position:absolute;top:-2px;left:{tg_pos}%;width:2px;height:16px;background:#1a365d;"></div>'
      f'</div></td></tr>'
    )

  # total row style dark
  html.append('</tbody></table></div>')

  # Combo + MBS colored cards
  co = combo_off or {}
  cn = combo_on or {}
  html.append(
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;">'
    '<style>@media(max-width:700px){div[data-hs-mbs]{grid-template-columns:1fr!important;}}</style>'
  )
  # force responsive via class
  html[-1] = (
    '<div data-hs-mbs="1" style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;">'
    '<style>@media(max-width:700px){[data-hs-mbs]{grid-template-columns:1fr!important;}}</style>'
  )

  html.append(
    f'<div style="background:linear-gradient(135deg,#ebf8ff,#fff);border:1px solid #90cdf4;'
    f'border-left:4px solid #3182ce;border-radius:12px;padding:14px;">'
    f'<div style="font-size:12px;font-weight:800;color:#2b6cb0;margin-bottom:6px;">ĐH COMBO</div>'
    f'<div style="font-size:13px;color:#2d3748;line-height:1.6;">'
    f'<span style="color:#3182ce;font-weight:700;">OFF:</span> '
    f'<b>{co.get("th",0)}</b> / {co.get("ct",0)} CH '
    f'(<span style="color:{_pct_color(co.get("pct",0), tg)};font-weight:700;">{co.get("pct",0):.1f}%</span>)<br/>'
    f'<span style="color:#dd6b20;font-weight:700;">ON:</span> '
    f'<b>{cn.get("th",0)}</b> / {cn.get("ct",0)} CH '
    f'(<span style="color:{_pct_color(cn.get("pct",0), tg)};font-weight:700;">{cn.get("pct",0):.1f}%</span>)'
    f'</div></div>'
  )

  def _mbs_block(title, info, accent):
    if not info:
      return (
        f'<div style="margin-bottom:8px;"><b style="color:{accent};">{title}</b>: không có data</div>'
      )
    parts = [f'<span style="background:#edf2f7;padding:1px 6px;border-radius:4px;margin:2px;display:inline-block;">{k}: {v}</span>'
             for k, v in info.get('groups', {}).items()]
    dat, total = info.get('dat', 0), info.get('total', 0)
    pct = (dat / total * 100) if total else 0
    return (
      f'<div style="margin-bottom:8px;"><b style="color:{accent};">{title}</b> · '
      f'<b>{dat}/{total}</b> đạt NV '
      f'(<span style="color:{_pct_color(pct, tg)};font-weight:700;">{pct:.1f}%</span>)</div>'
      f'<div style="font-size:12px;color:#4a5568;">{"".join(parts)}</div>'
    )

  html.append(
    f'<div style="background:linear-gradient(135deg,#faf5ff,#fff);border:1px solid #d6bcfa;'
    f'border-left:4px solid #805ad5;border-radius:12px;padding:14px;">'
    f'<div style="font-size:12px;font-weight:800;color:#6b46c1;margin-bottom:6px;">MBS CAT &amp; BRAND</div>'
    f'<div style="font-size:13px;color:#2d3748;line-height:1.5;">'
    f'{_mbs_block("MBS Cat", mbs_cat, "#805ad5")}'
    f'{_mbs_block("MBS Brand", mbs_brand, "#d53f8c")}'
    f'</div></div>'
  )
  html.append('</div></div>')
  return ''.join(html)


def build_hs_monthly_kpi_rows(df, report_date, targets, turnover_targets, filter_nv, mcp_df):
  """Lấy TH/CT/% MTD các KPI tháng."""
  rows = []
  try:
    df_to, _, _ = build_turnover_report(df, report_date, turnover_targets, filter_nv)
    if df_to is not None and not df_to.empty and 'Tên NVBH' in df_to.columns:
      body = df_to[~df_to['Tên NVBH'].astype(str).str.upper().str.contains('TOTAL|TỔNG', na=False, regex=True)]
      ct = float(pd.to_numeric(body['Chỉ Tiêu Doanh Số'], errors='coerce').fillna(0).sum()) if 'Chỉ Tiêu Doanh Số' in body.columns else 0
      th = float(pd.to_numeric(body['Doanh Số MTD'], errors='coerce').fillna(0).sum()) if 'Doanh Số MTD' in body.columns else 0
      rows.append({'name': 'Doanh số', 'th': th, 'ct': ct, 'pct': (th/ct*100 if ct else 0), 'fmt': 'money'})
    else:
      rows.append({'name': 'Doanh số', 'th': 0, 'ct': 0, 'pct': 0, 'fmt': 'money'})
  except Exception:
    rows.append({'name': 'Doanh số', 'th': 0, 'ct': 0, 'pct': 0, 'fmt': 'money'})

  # PC BT / Call Plan OFF
  # CT tháng = Σ (Plan VT OFF mỗi ngày bán hàng trong tháng)
  # Plan ngày = số CH OFF có lịch VT đúng ngày đó (giống metric card Hiệu Suất)
  try:
    df_pc, _, _ = build_report(df, report_date, targets, 'PC_BT', filter_nv, mcp_df=mcp_df)
    th_pc = 0.0
    if df_pc is not None and not df_pc.empty:
      name_col = 'Tên NVBH' if 'Tên NVBH' in df_pc.columns else None
      body = df_pc
      if name_col:
        body = df_pc[~df_pc[name_col].astype(str).str.upper().str.contains('TOTAL|TỔNG', na=False, regex=True)]
      col_mtd = None
      for c in body.columns:
        cl = str(c).lower().strip()
        if cl == 'mtd' or cl == 'thực hiện' or cl.startswith('mtd'):
          col_mtd = c
          break
      if col_mtd:
        th_pc = float(pd.to_numeric(body[col_mtd], errors='coerce').fillna(0).sum())

    y, mth = report_date.year, report_date.month
    # Chỉ cộng đến ngày xem báo cáo (MTD), không lấy full tháng
    rd = report_date.date() if hasattr(report_date, 'date') else report_date
    n_days = int(rd.day) if getattr(rd, 'month', mth) == mth and getattr(rd, 'year', y) == y else calendar.monthrange(y, mth)[1]
    ch_map = build_mcp_channel_map(mcp_df) if mcp_df is not None else {}

    def _thu_to_weekdays(thu_val):
      s = str(thu_val).strip().replace('.0', '')
      mapping = {
          '2': {0}, '3': {1}, '4': {2}, '5': {3}, '6': {4}, '7': {5},
          '25': {0, 3}, '36': {1, 4}, '47': {2, 5},
      }
      if s in mapping:
        return set(mapping[s])
      wds = set()
      for k, v in mapping.items():
        if k in s:
          wds |= v
      return wds

    # --- A. Từ file lịch VT: cộng Plan OFF từng ngày ---
    plan_from_sched = 0
    try:
      vs = load_visit_schedule()
    except Exception:
      vs = None
    if vs is not None and not isinstance(vs, str) and hasattr(vs, 'empty') and not vs.empty:
      v = vs.copy()
      c_ma = find_col(v, ['Mã CH', 'Outlet_code', 'Outlet Code', 'Mã KH'])
      c_nv = find_col(v, ['Tên NVBH', 'Tên NV', 'SM name', 'Nhân viên', 'Tên ĐDKD'])
      if c_ma:
        v['_ma'] = v[c_ma].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
      if '_plan_date' not in v.columns:
        c_pd = find_col(v, ['Ngày lịch VT', 'Ngày VT', 'Plan Date'])
        if c_pd:
          v['_plan_date'] = pd.to_datetime(v[c_pd], dayfirst=True, errors='coerce').dt.date
      if '_plan_date' in v.columns:
        v = v[v['_plan_date'].apply(
            lambda x: bool(x) and getattr(x, 'year', None) == y and getattr(x, 'month', None) == mth
        )]
      if filter_nv and c_nv and not v.empty:
        if isinstance(filter_nv, (list, tuple, set)):
          v = v[v[c_nv].astype(str).str.strip().isin([str(x).strip() for x in filter_nv])]
        else:
          v = v[v[c_nv].astype(str).str.contains(str(filter_nv), case=False, na=False)]
      # Cộng từng ngày: unique CH OFF / ngày
      if '_plan_date' in v.columns and '_ma' in v.columns:
        for day in range(1, n_days + 1):
          dt = date(y, mth, day)
          if dt.weekday() >= 6:
            continue
          day_set = set()
          for _, r in v[v['_plan_date'] == dt].iterrows():
            ma = str(r.get('_ma', '')).strip()
            if not ma or ma.lower() in ('nan', 'none'):
              continue
            if ch_map.get(ma) == 'ON':
              continue
            day_set.add(ma)
          plan_from_sched += len(day_set)

    # --- B. Từ MCP Thứ VT: cộng Plan OFF từng ngày (chuẩn khi lịch file thiếu) ---
    plan_from_mcp = 0
    if mcp_df is not None and not mcp_df.empty:
      m = mcp_df.copy()
      c_ma = find_col(m, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Ma CH'])
      c_sm = find_col(m, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
      c_thu = find_col(m, [
          'Thứ VT', 'Thu VT', 'Ngày VT', 'Visit Day', 'F',
          'Tần suất', 'Tan suat', 'Frequency', 'Thứ',
      ])
      if filter_nv and c_sm:
        if isinstance(filter_nv, (list, tuple, set)):
          m = m[m[c_sm].astype(str).str.strip().isin([str(x).strip() for x in filter_nv])]
        else:
          m = m[m[c_sm].astype(str).str.contains(str(filter_nv), case=False, na=False)]
      ma_wds = {}
      if c_ma is not None:
        for _, r in m.iterrows():
          ma = str(r[c_ma]).strip().replace('.0', '')
          if not ma or ma.lower() in ('nan', 'none'):
            continue
          if ch_map.get(ma) == 'ON':
            continue
          wds = _thu_to_weekdays(r[c_thu]) if c_thu is not None else set()
          if not wds:
            wds = {0, 3}  # mặc định F4: T2+T5
          if ma not in ma_wds:
            ma_wds[ma] = set()
          ma_wds[ma] |= wds
      for day in range(1, n_days + 1):
        dt = date(y, mth, day)
        wd = dt.weekday()
        if wd >= 6:
          continue
        plan_from_mcp += sum(1 for ma, wds in ma_wds.items() if wd in wds)

    # Ưu tiên nguồn lớn hơn (lịch file thường thiếu ngày)
    call_plan_off = max(plan_from_sched, plan_from_mcp)
    pct_pc = (th_pc / call_plan_off * 100) if call_plan_off else 0
    rows.append({
        'name': 'PC BT / Call Plan OFF',
        'th': th_pc,
        'ct': call_plan_off,
        'pct': pct_pc,
        'fmt': 'num',
    })
  except Exception:
    rows.append({'name': 'PC BT / Call Plan OFF', 'th': 0, 'ct': 0, 'pct': 0, 'fmt': 'num'})

  kpi_list = [
    ('PC_BT', 'PC BT', 'num'),
    ('LPPC', 'LPPC OFF (trừ Meat, Beer)', 'float'),
    ('ASO_ALL', 'ASO ALL', 'num'),
    ('ASO_FOCUS', 'Trận Xanh · Tea365', 'num'),
    ('ASO_FOCUS_2', 'Trận Vàng · Homey', 'num'),
    ('PC_ON', 'PC ON', 'num'),
    ('LPPC_MEAT', 'LPPC Meat', 'float'),
  ]
  for rt, label, fmt in kpi_list:
    try:
      df_k, _, _ = build_report(df, report_date, targets, rt, filter_nv, mcp_df=mcp_df)
      if df_k is None or df_k.empty:
        rows.append({'name': label, 'th': 0, 'ct': 0, 'pct': 0, 'fmt': fmt})
        continue
      name_col = 'Tên NVBH' if 'Tên NVBH' in df_k.columns else None
      body = df_k
      if name_col:
        body = df_k[~df_k[name_col].astype(str).str.upper().str.contains('TOTAL|TỔNG', na=False, regex=True)]
      col_ct = col_mtd = None
      for c in body.columns:
        cl = str(c).lower()
        if col_ct is None and ('chỉ tiêu' in cl or 'chi tieu' in cl):
          col_ct = c
        if col_mtd is None and (cl == 'mtd' or 'doanh số mtd' in cl or cl == 'thực hiện'):
          col_mtd = c
      if col_mtd is None and 'MTD' in body.columns:
        col_mtd = 'MTD'
      if fmt == 'float':
        th = float(pd.to_numeric(body[col_mtd], errors='coerce').fillna(0).mean()) if col_mtd else 0
        ct = float(pd.to_numeric(body[col_ct], errors='coerce').fillna(0).mean()) if col_ct else 0
        if ct == 0:
          ct = 3.8 if rt == 'LPPC_MEAT' else float(get_month_cfg().get('lppc_moc', 4.3) or 4.3)
      else:
        th = float(pd.to_numeric(body[col_mtd], errors='coerce').fillna(0).sum()) if col_mtd else 0
        ct = float(pd.to_numeric(body[col_ct], errors='coerce').fillna(0).sum()) if col_ct else 0
      pct = (th / ct * 100) if ct else 0
      rows.append({'name': label, 'th': th, 'ct': ct, 'pct': pct, 'fmt': fmt})
    except Exception:
      rows.append({'name': label, 'th': 0, 'ct': 0, 'pct': 0, 'fmt': fmt})
  return rows


def build_hs_combo_mbs_summary(df, report_date, df_combo_off, df_combo_on, cat_df, brand_df, mcp_df, filter_nv):
  """Combo OFF/ON + MBS Cat/Brand summary."""
  combo_off, combo_on = {'th': 0, 'ct': 0, 'pct': 0}, {'th': 0, 'ct': 0, 'pct': 0}
  try:
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy() if df is not None and not df.empty else pd.DataFrame()
    if nv_selected(filter_nv) and not df_mtd.empty:
      df_mtd = filter_df_by_nv(df_mtd, 'Tên NVBH', filter_nv)
    combo = tag_combo_orders_t10(df_mtd, mcp_df=mcp_df)
    if combo is not None and not combo.empty and 'Mã CH' in combo.columns:
      ch = combo['channel'].astype(str).str.upper() if 'channel' in combo.columns else pd.Series('OFF', index=combo.index)
      off_ch = int(combo.loc[ch.str.contains('OFF', na=False), 'Mã CH'].nunique())
      on_ch = int(combo.loc[ch.str.contains('ON', na=False) & ~ch.str.contains('OFF', na=False), 'Mã CH'].nunique())
    else:
      off_ch = on_ch = 0

    def _tgt(raw):
      if raw is None or getattr(raw, 'empty', True):
        return 0
      c_ma = find_col(raw, ['outlet_code', 'Outlet Code', 'Mã CH'])
      if not c_ma:
        return 0
      d = raw
      if nv_selected(filter_nv):
        c_nv = find_col(raw, ['Tên NV', 'SM name', 'Tên NVBH', 'Nhân viên'])
        if c_nv:
          d = filter_df_by_nv(raw, c_nv, filter_nv)
      return int(d[c_ma].nunique()) if c_ma in d.columns else 0

    ct_off, ct_on = _tgt(df_combo_off), _tgt(df_combo_on)
    combo_off = {'th': off_ch, 'ct': ct_off, 'pct': (off_ch/ct_off*100 if ct_off else 0)}
    combo_on = {'th': on_ch, 'ct': ct_on, 'pct': (on_ch/ct_on*100 if ct_on else 0)}
  except Exception:
    pass

  def _mbs_info(mbs_df):
    if mbs_df is None or getattr(mbs_df, 'empty', True):
      return None
    d = mbs_df.copy()
    c_nv = find_col(d, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    if nv_selected(filter_nv) and c_nv:
      d = filter_df_by_nv(d, c_nv, filter_nv)
    c_type = find_col(d, ['Member Type', 'Member type', 'Loại', 'Group', 'Nhóm'])
    c_actual = find_col(d, [
        'Doanh số thực đạt của CAT', 'Doanh số thực đạt CAT',
        'Doanh số thực đạt của BRAND', 'Doanh số thực đạt BRAND',
        'Doanh số thực đạt', 'Actual',
    ])
    c_ct = find_col(d, [
        'Doanh số nền tảng của OUTLET', 'Chỉ tiêu của CAT', 'Chỉ tiêu CAT',
        'Chỉ tiêu của BRAND', 'Chỉ tiêu BRAND', 'Target',
    ])
    groups = {}
    dat = total = 0
    if c_type:
      for gname, gdf in d.groupby(d[c_type].astype(str).str.strip()):
        if not gname or gname.lower() in ('nan', 'none', ''):
          continue
        n = len(gdf)
        n_dat = 0
        if c_actual and c_ct:
          act = pd.to_numeric(gdf[c_actual], errors='coerce').fillna(0)
          ct = pd.to_numeric(gdf[c_ct], errors='coerce').fillna(0)
          n_dat = int(((act >= ct) & (ct > 0)).sum())
        groups[gname] = f'{n_dat}/{n}'
        dat += n_dat
        total += n
    else:
      total = len(d)
    return {'groups': groups, 'dat': dat, 'total': total}

  return combo_off, combo_on, _mbs_info(cat_df), _mbs_info(brand_df)

def render_performance_html(df):
  if df is None or df.empty:
    return '<p>Không có dữ liệu hiệu suất.</p>'
  return (
      _perf_table_html(df, 'call')
      + _perf_table_html(df, 'fund')
  )


# ====================== GIAO DIỆN ======================
st.markdown(
    f"""
<div class="main-header">
    <div class="logo">{logo_svg}</div>
    <div class="title-block">
        <h1>SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</h1>
        <h2>TRACKING KPI ĐDKD - TEAM SS TRƯƠNG THANH TÂN </h2>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

col_reload, col_empty = st.columns([2, 5])
with col_reload:
  if st.button('🔄 Xóa Cache & Reload Dữ Liệu'):
    st.cache_data.clear()
    st.rerun()

with st.spinner('Đang tải dữ liệu...'):
  df, mcp = load_main_data()
  targets = get_targets()
  turnover_targets = get_turnover_targets()
  df_cat = load_cat_data()
  df_brand = load_brand_data()
  df_combo_off, df_combo_on = load_combo_data()
  df_visit_sched = load_visit_schedule()

  mcp = process_mcp_sales(df, mcp)
  df_cat = process_cat_sales(df, df_cat)
  df_brand = process_brand_sales(df, df_brand)

# Full NV list: RPT + Target_KPI + MCP (NV chưa bán vẫn chọn được / hiện 0)
_nv_set = set()
if not df.empty and 'Tên NVBH' in df.columns:
  _nv_set.update(df['Tên NVBH'].dropna().astype(str).str.strip().tolist())
_roster = get_all_sm_roster()
_nv_set.update([n for n in _roster.values() if n])
if mcp is not None and not mcp.empty:
  _c_nm = find_col(mcp, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
  if _c_nm:
    _nv_set.update(mcp[_c_nm].dropna().astype(str).str.strip().tolist())
_bad_nv = {
    'sm name', 'sm name', 'sm code', 'smcode', 'tên nvbh', 'mã nvbh',
    'nhân viên', 'nan', 'none', '',
}
nv_list = sorted(
    [x for x in _nv_set if x and x.lower() not in _bad_nv]
)

vn_time = dt.datetime.utcnow() + dt.timedelta(hours=7)
_default_t1 = (vn_time - timedelta(days=1)).date()
# Mặc định theo tháng báo cáo đang chạy: T10/2026
_REPORT_MONTH_START = date(2026, 10, 1)
_REPORT_MONTH_END = date(2026, 10, 31)
if _default_t1 < _REPORT_MONTH_START:
  default_date_t_minus_1 = _REPORT_MONTH_START
elif _default_t1 > _REPORT_MONTH_END:
  default_date_t_minus_1 = _REPORT_MONTH_END
else:
  default_date_t_minus_1 = _default_t1


def get_timegone_stats(target_date):
  year = target_date.year
  month = target_date.month
  first_day = dt.date(year, month, 1)
  if month == 12:
    last_day = dt.date(year + 1, 1, 1) - timedelta(days=1)
  else:
    last_day = dt.date(year, month + 1, 1) - timedelta(days=1)

  total_working_days = 0
  elapsed_working_days = 0

  # Ngày nghỉ lễ theo tháng (logic cũ: trừ CN + lễ)
  # T9/2026: 01-02/09 Quốc khánh; T10/2026: không có lễ cố định
  holidays_by_month = {
      (2026, 9): {1, 2},
      (2026, 10): set(),
  }
  holiday_days = holidays_by_month.get((year, month), set())

  curr = first_day
  while curr <= last_day:
    is_sunday = curr.weekday() == 6
    is_holiday = curr.day in holiday_days

    if not is_sunday and not is_holiday:
      total_working_days += 1
      if curr <= target_date:
        elapsed_working_days += 1
    curr += timedelta(days=1)

  remaining_working_days = total_working_days - elapsed_working_days
  pct_timegone = (
      round(elapsed_working_days / total_working_days * 100, 1)
      if total_working_days > 0
      else 0
  )
  return (
      total_working_days,
      elapsed_working_days,
      remaining_working_days,
      pct_timegone,
  )


# ===== Chọn tháng báo cáo (data/Thang09 | data/Thang10) =====
if 'report_month_key' not in st.session_state:
  st.session_state['report_month_key'] = 'Thang10'

_month_labels = {k: v['label'] for k, v in MONTH_OPTIONS.items()}
_month_keys = list(MONTH_OPTIONS.keys())
_cur_idx = _month_keys.index(st.session_state['report_month_key']) if st.session_state['report_month_key'] in _month_keys else 1

mc1, mc2 = st.columns([1, 3])
with mc1:
  st.markdown('<p class="filter-label">📅 Tháng báo cáo</p>', unsafe_allow_html=True)
  _sel_label = st.selectbox(
      'Tháng',
      options=[_month_labels[k] for k in _month_keys],
      index=_cur_idx,
      key='month_select_box',
      label_visibility='collapsed',
  )
_new_key = [k for k, v in MONTH_OPTIONS.items() if v['label'] == _sel_label][0]
if _new_key != st.session_state.get('report_month_key'):
  st.session_state['report_month_key'] = _new_key
  # Đổi tháng → clear cache data
  try:
    load_main_data.clear()
  except Exception:
    pass
  try:
    st.cache_data.clear()
  except Exception:
    pass
  _refresh_paths()
  st.rerun()

_cfg_m = get_month_cfg()
_y, _m = _cfg_m['year'], _cfg_m['month']
_month_start = date(_y, _m, 1)
if _m == 12:
  _month_end = date(_y + 1, 1, 1) - timedelta(days=1)
else:
  _month_end = date(_y, _m + 1, 1) - timedelta(days=1)

# Ngày báo cáo (lấy từ session để tính Timegone trước khi vẽ filter)
report_date = st.session_state.get('ngay', default_date_t_minus_1)
if not isinstance(report_date, date):
  try:
    report_date = date.fromisoformat(str(report_date)[:10])
  except Exception:
    report_date = default_date_t_minus_1
# Clamp trong tháng đang chọn
if report_date < _month_start:
  report_date = _month_start
elif report_date > _month_end:
  report_date = min(_month_end, default_date_t_minus_1) if default_date_t_minus_1 >= _month_start else _month_end
st.session_state['ngay'] = report_date

_refresh_paths()
tot_days, elapsed_days, remain_days, pct_tg = get_timegone_stats(report_date)

# Bảng Metric tiến độ — NẰM TRÊN các bộ lọc
st.markdown(
    f"""
<div class="timegone-container" style="background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; margin: 5px 0 12px 0; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <div class="timegone-title" style="font-weight: 800; color: #1a365d; font-size: 12.5px; margin-bottom: 6px;">⏳ TIẾN ĐỘ THỜI GIAN THÁNG {report_date.strftime('%m/%Y')}</div>
    <div class="timegone-grid" style="display: flex; justify-content: space-around; font-size: 11.5px; gap: 6px; flex-wrap: wrap;">
        <div class="timegone-item" style="background: #fff; padding: 3px 8px; border-radius: 4px; border: 1px solid #edf2f7;"><b>Tổng làm việc:</b> <span style="color: #2b6cb0; font-weight: 700;">{tot_days}</span></div>
        <div class="timegone-item" style="background: #fff; padding: 3px 8px; border-radius: 4px; border: 1px solid #edf2f7;"><b>Đã trôi qua:</b> <span style="color: #c53030; font-weight: 700;">{elapsed_days}</span></div>
        <div class="timegone-item" style="background: #fff; padding: 3px 8px; border-radius: 4px; border: 1px solid #edf2f7;"><b>Còn lại:</b> <span style="color: #2f855a; font-weight: 700;">{remain_days}</span></div>
        <div class="timegone-item" style="background: #c6f6d5; padding: 3px 8px; border-radius: 4px; border: 1px solid #9ae6b4; color: #22543d;"><b>% Timegone:</b> <span style="font-weight: 800;">{pct_tg}%</span></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Bộ lọc chính
# Danh sách Mã KH / Tên KH (từ MCP + RPT) — multiselect: gõ tìm + chọn nhiều
_ma_set, _ten_set = set(), set()
if mcp is not None and not mcp.empty:
  _c_ma = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH', 'outlet_code'])
  _c_ten = find_col(
      mcp,
      ['Outlet Name', 'Outlet_Name', 'Tên CH', 'Tên khách hàng', 'Customer Name', 'Tên KH'],
  )
  if _c_ma:
    _ma_set.update(mcp[_c_ma].dropna().astype(str).str.strip().tolist())
  if _c_ten:
    _ten_set.update(mcp[_c_ten].dropna().astype(str).str.strip().tolist())
if df is not None and not df.empty:
  if 'Mã CH' in df.columns:
    _ma_set.update(df['Mã CH'].dropna().astype(str).str.strip().tolist())
  _c_ten_rpt = find_col(df, ['Tên CH', 'Tên khách hàng', 'Outlet Name', 'Tên KH'])
  if _c_ten_rpt:
    _ten_set.update(df[_c_ten_rpt].dropna().astype(str).str.strip().tolist())
_bad = {'nan', 'none', '', 'mã ch', 'outlet_code', 'outlet code', 'tên ch'}
ma_opts = sorted([x for x in _ma_set if x and x.lower() not in _bad])
ten_opts = sorted([x for x in _ten_set if x and x.lower() not in _bad])

# Hàng 1: Ngày - KPI Name - ĐDKD
f1, f2, f3 = st.columns([1, 1.3, 1])
with f1:
  st.markdown('<p class="filter-label">NGÀY</p>', unsafe_allow_html=True)
  report_date = st.date_input(
      '',
      value=report_date,
      min_value=_month_start,
      max_value=_month_end,
      key='ngay',
      label_visibility='collapsed',
  )
  tot_days, elapsed_days, remain_days, pct_tg = get_timegone_stats(report_date)
  set_timegone_color_context(pct_tg)
with f2:
  st.markdown('<p class="filter-label">KPI NAME</p>', unsafe_allow_html=True)
  # Mức lương + tên KPI theo tháng đang chọn (T09: CV17+20 | T10: CV22)
  KPI_SALARY_LABEL = dict(get_month_cfg().get('salary', {}))
  _cfg = get_month_cfg()
  _f1 = _cfg.get('aso_focus_name', 'ASO_Focus')
  _f2 = _cfg.get('aso_focus2_name', 'ASO_Focus_2')
  _pon = _cfg.get('pc_on_name', 'PC_ON')
  kpi_map = {
      # ===== 8 KPI theo tháng =====
      '1. TURNOVER - Tổng doanh số bán ra': 'TURNOVER',
      '2. PC_BT - Đơn hàng ≥4 line MOQ (L1 OFF)': 'PC_BT',
      '3. LPPC - Bình quân line/PC (trừ Meat & Beer)': 'LPPC',
      f"4. {_cfg.get('aso_all_name', 'ASO_ALL')}": 'ASO_ALL',
      f'5. {_f1}': 'ASO_FOCUS',
      f'6. {_f2}': 'ASO_FOCUS_2',
      f'7. {_pon}': 'PC_ON',
      '8. LPPC_Meat - Bình quân line/PC (Processed Meats)': 'LPPC_MEAT',
      # ===== Báo cáo giữ logic Tháng 9 =====
      '9. BÁO CÁO ĐH COMBO': 'COMBO',
      '10. BÁO CÁO TỔNG HỢP': 'SUMMARY',
      '11. BÁO CÁO LỊCH VIẾNG THĂM': 'VISIT',
      '12. BÁO CÁO MBS CAT': 'MBS_CAT',
      '13. BÁO CÁO MBS BRAND': 'MBS_BRAND',
      '14. BÁO CÁO HIỆU SUẤT BÁN HÀNG': 'PERFORMANCE',
      '15. BÁO CÁO TRƯNG BÀY': 'DISPLAY',
      '16. KẾ HOẠCH TÁC CHIẾN TRÀ BÚP NON T10': 'TEA_BATTLE',
      '17. BÁO CÁO PERFORMANCE': 'PERF_CAT',
      '18. WEEKLY PREVIEW - MCP / ASO / %COV': 'WEEKLY_PREVIEW',
  }
  selected_name = st.selectbox(
      '',
      list(kpi_map.keys()),
      key=f"kpi_{get_month_key()}",
      label_visibility='collapsed',
  )
  selected_kpi = kpi_map[selected_name]
with f3:
  st.markdown(
      '<p class="filter-label">ĐDKD (Nhân viên - Chọn nhiều)</p>',
      unsafe_allow_html=True,
  )
  filter_nv = st.multiselect(
      '',
      nv_list,
      default=[],
      key='ddkd',
      label_visibility='collapsed',
      placeholder='Tất cả ĐDKD',
  )

# Hàng 2: Thứ VT - Mã Khách Hàng - Tên Khách Hàng
f4, f5, f6 = st.columns([1, 1, 1])
with f4:
  st.markdown(
      '<p class="filter-label">📅 Thứ VT (MBS CAT/BRAND)</p>', unsafe_allow_html=True
  )
  thu_opts_main = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
  f_thu_vt_main = st.multiselect(
      '',
      thu_opts_main,
      default=[],
      key='mbs_cat_thu_filter',
      label_visibility='collapsed',
      placeholder='Tất cả các thứ',
      disabled=(selected_kpi not in ['MBS_CAT', 'MBS_BRAND']),
  )
with f5:
  st.markdown('<p class="filter-label">🆔 Mã Khách Hàng</p>', unsafe_allow_html=True)
  filter_ma_kh_raw = st.text_input(
      '',
      value='',
      key='filter_ma_kh',
      label_visibility='collapsed',
      placeholder='Nhập mã KH rồi Enter (nhiều mã cách nhau bởi dấu phẩy)',
  )
with f6:
  st.markdown('<p class="filter-label">🏪 Tên Khách Hàng</p>', unsafe_allow_html=True)
  filter_ten_kh_raw = st.text_input(
      '',
      value='',
      key='filter_ten_kh',
      label_visibility='collapsed',
      placeholder='Nhập tên KH rồi Enter (nhiều tên cách nhau bởi dấu phẩy)',
  )

# Parse input: hỗ trợ nhiều giá trị cách nhau bởi dấu phẩy / ;
def _parse_kh_input(raw):
  if not raw or not str(raw).strip():
    return []
  parts = []
  for p in str(raw).replace(';', ',').split(','):
    p = p.strip()
    if p:
      parts.append(p)
  return parts

filter_ma_kh = _parse_kh_input(filter_ma_kh_raw)
filter_ten_kh = _parse_kh_input(filter_ten_kh_raw)

# Áp dụng lọc Mã KH / Tên KH lên data trước khi chạy báo cáo
def _apply_kh_filter(df_src, ma_list, ten_list):
  """Lọc theo Mã KH / Tên KH (partial match, không phân biệt hoa thường)."""
  if df_src is None or df_src.empty:
    return df_src
  out = df_src
  if ma_list:
    c_ma = find_col(out, ['Mã CH', 'Outlet_code', 'Outlet Code', 'outlet_code'])
    if c_ma:
      s = out[c_ma].astype(str).str.strip().str.lower()
      mask = False
      for x in ma_list:
        mask = mask | s.str.contains(str(x).strip().lower(), na=False, regex=False)
      out = out[mask]
  if ten_list:
    c_ten = find_col(
        out,
        ['Tên CH', 'Tên khách hàng', 'Outlet Name', 'Outlet_Name', 'Tên KH', 'Customer Name'],
    )
    if c_ten:
      s = out[c_ten].astype(str).str.strip().str.lower()
      mask = False
      for x in ten_list:
        mask = mask | s.str.contains(str(x).strip().lower(), na=False, regex=False)
      out = out[mask]
  return out

if filter_ma_kh or filter_ten_kh:
  df = _apply_kh_filter(df, filter_ma_kh, filter_ten_kh)
  if mcp is not None and not mcp.empty:
    mcp = _apply_kh_filter(mcp, filter_ma_kh, filter_ten_kh)
  if 'df_cat' in dir() and df_cat is not None and not df_cat.empty:
    df_cat = _apply_kh_filter(df_cat, filter_ma_kh, filter_ten_kh)
  if 'df_brand' in dir() and df_brand is not None and not df_brand.empty:
    df_brand = _apply_kh_filter(df_brand, filter_ma_kh, filter_ten_kh)


# Mobile: chặn bàn phím trên select/date — vẫn mở được dropdown/calendar
# Chỉ text_input (Mã KH / Tên KH) mới cho gõ
components.html(
    """
<script>
(function() {
  var doc = window.parent.document;

  function lockSelectOrDate(el) {
    if (!el) return;
    try {
      el.setAttribute('readonly', 'true');
      el.setAttribute('inputmode', 'none');
      el.setAttribute('autocomplete', 'off');
      el.style.caretColor = 'transparent';
      // KHÔNG pointer-events:none, KHÔNG blur — để dropdown/calendar mở bình thường
      if (!el._kbLockBound) {
        el._kbLockBound = true;
        var keep = function() {
          this.setAttribute('readonly', 'true');
          this.setAttribute('inputmode', 'none');
          this.style.caretColor = 'transparent';
        };
        el.addEventListener('touchstart', keep, true);
        el.addEventListener('touchend', keep, true);
        el.addEventListener('focus', keep, true);
        el.addEventListener('keydown', function(e) {
          // Chặn gõ phím ảo / hardware trên select-date
          if (e.key && e.key.length === 1) e.preventDefault();
        }, true);
      }
    } catch (err) {}
  }

  function apply() {
    try {
      doc.querySelectorAll(
        '[data-baseweb="select"] input, [data-testid="stSelectbox"] input, [data-testid="stMultiSelect"] input'
      ).forEach(lockSelectOrDate);

      doc.querySelectorAll('[data-testid="stDateInput"] input').forEach(lockSelectOrDate);

      // Text input: cho gõ
      doc.querySelectorAll('[data-testid="stTextInput"] input').forEach(function(el) {
        el.removeAttribute('readonly');
        if (el.getAttribute('inputmode') === 'none') {
          el.setAttribute('inputmode', 'text');
        }
        el.style.caretColor = 'auto';
      });
    } catch (err) {}
  }

  apply();
  setInterval(apply, 600);
  try {
    var obs = new MutationObserver(function() { apply(); });
    obs.observe(doc.body, { childList: true, subtree: true });
  } catch (err) {}
  doc.addEventListener('touchstart', function() { setTimeout(apply, 20); }, true);
})();
</script>
""",
    height=0,
    width=0,
)


st.markdown('---')

tab_kpi, tab_mcp, tab_cat, tab_brand, tab_dskh_off, tab_dskh_on = st.tabs([
    '📊 BÁO CÁO KPI',
    '🗺️ MCP VISIT',
    '📦 TRACKING MBS - CAT',
    '🏷️ TRACKING MBS - BRAND',
    '📋 DSKH_Combo OFF',
    '📋 DSKH_Combo ON',
])

# ----- TAB KPI -----
with tab_kpi:
  # Báo cáo hỗ trợ lọc Mã KH / Tên KH (có thông tin cửa hàng)
  _KPI_SUPPORT_KH = {
      'MBS_CAT', 'MBS_BRAND', 'VISIT', 'COMBO', 'SUMMARY',
  }
  _kh_filter_active = bool(filter_ma_kh or filter_ten_kh)
  if _kh_filter_active and selected_kpi not in _KPI_SUPPORT_KH:
    st.markdown(
        """
        <div style="background:#fff5f5;border:1px solid #feb2b2;border-radius:10px;
                    padding:28px 20px;text-align:center;margin:24px 0;">
          <div style="font-size:18px;font-weight:800;color:#c53030;margin-bottom:8px;">
            Vui Lòng Chọn Báo Cáo Phù Hợp Với Nội Dung Cần Xem
          </div>
          <div style="font-size:13px;color:#4a5568;">
            Bộ lọc <b>Mã Khách Hàng</b> / <b>Tên Khách Hàng</b> chỉ áp dụng cho:
            <b>ĐH Combo, Tổng Hợp, Lịch Viếng Thăm, MBS CAT, MBS Brand</b>
            và các tab MCP / Tracking.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  elif selected_kpi == 'SUMMARY':
    set_color_moc_for_kpi('SUMMARY')
    saved_sum_thu = st.query_params.get('sum_thu', '')
    default_sum_thu_list = (
        [x.strip() for x in saved_sum_thu.split(',') if x.strip()]
        if saved_sum_thu
        else []
    )

    if not default_sum_thu_list and report_date:
      wday = report_date.weekday()
      if wday in [0, 3]:
        default_sum_thu_list = ['25']
      elif wday in [1, 4]:
        default_sum_thu_list = ['36']
      elif wday in [2, 5]:
        default_sum_thu_list = ['47']

    def update_sum_params():
      st.query_params['sum_thu'] = (
          ','.join(st.session_state.sum_thu_input)
          if st.session_state.sum_thu_input
          else ''
      )

    col_f_thu, col_f_metrics = st.columns([1, 1.5])
    with col_f_thu:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ / Chu kỳ (Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      valid_sum_thu = [t for t in default_sum_thu_list if t in thu_opts]
      f_thu_sum = st.multiselect(
          '',
          thu_opts,
          default=valid_sum_thu,
          key='sum_thu_input',
          on_change=update_sum_params,
          label_visibility='collapsed',
      )

    with col_f_metrics:
      st.markdown(
          '<p class="filter-label">📊 Chọn Chỉ Số Hiển Thị</p>',
          unsafe_allow_html=True,
      )
      metric_opts = [
          'VIP MCH',
          'Doanh Số',
          'PC BT',
          'LPPC',
          'ASO Trận Xanh',
          'ASO Trận Vàng',
          'PC Kênh ON',
          'KH Combo OFF',
          'KH Combo ON',
          'MBS Cat',
          'MBS Brand',
      ]
      saved_metrics = st.query_params.get('sum_metrics', '')
      default_metrics = (
          [x.strip() for x in saved_metrics.split(',') if x.strip()]
          if saved_metrics
          else metric_opts
      )
      valid_metrics = [m for m in default_metrics if m in metric_opts]
      if not valid_metrics:
        valid_metrics = metric_opts

      def update_metric_params():
        st.query_params['sum_metrics'] = (
            ','.join(st.session_state.sum_metrics_input)
            if st.session_state.sum_metrics_input
            else ''
        )

      selected_metrics = st.multiselect(
          '',
          metric_opts,
          default=valid_metrics,
          key='sum_metrics_input',
          on_change=update_metric_params,
          label_visibility='collapsed',
      )
      if not selected_metrics:
        selected_metrics = metric_opts

    st.query_params['sum_thu'] = (
        ','.join(st.session_state.sum_thu_input)
        if st.session_state.sum_thu_input
        else ''
    )
    st.query_params['sum_metrics'] = ','.join(selected_metrics)

    try:
      _tg = get_targets()
    except Exception:
      _tg = {}
    df_summary = build_summary_report(
        df,
        report_date,
        df_combo_off,
        df_combo_on,
        df_cat,
        df_brand,
        mcp,
        filter_nv,
        f_thu_sum,
        targets=_tg,
    )
    tot_row_s = df_summary.iloc[-1]

    st.markdown(
        f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px;'
        f' font-size: 16px; text-align: center;">BÁO CÁO TỔNG HỢP - THÁNG'
        f' {report_date.strftime("%m/%Y")}</h3>',
        unsafe_allow_html=True,
    )
    st.caption(
        f"⚡ Ngày: {report_date.strftime('%d/%m/%Y')} | Lọc NV: {nv_label(filter_nv)} |"
        f" Lọc Thứ/Chu kỳ: {f_thu_sum if f_thu_sum else 'Tất cả'}"
    )

    # Metric cards theo KPI đang chọn — format TH/CT/%MTD
    def _fmt_num(v, as_float=False, money=False):
      try:
        if pd.isna(v) or v == '':
          return '0'
        x = float(v)
        if money:
          return f'{int(round(x)):,}'.replace(',', '.')
        if as_float:
          s = f'{x:.2f}'.rstrip('0').rstrip('.')
          return s
        return f'{int(round(x)):,}'.replace(',', '.')
      except Exception:
        return str(v) if v is not None else '0'

    def _card_th_ct_pct(th_col, ct_col, pct_col, as_float=False, money=False):
      th = _fmt_num(tot_row_s.get(th_col, 0), as_float=as_float, money=money)
      ct = _fmt_num(tot_row_s.get(ct_col, 0), as_float=as_float, money=money)
      pct = str(tot_row_s.get(pct_col, '0%'))
      if pct and not str(pct).endswith('%'):
        pct = f'{pct}%'
      return f'{th}/{ct}/{pct}'

    cards = []
    if 'VIP MCH' in selected_metrics:
      cards.append((
          'VIP MCH',
          _card_th_ct_pct('Đã Mua (VIP)', 'VIP MCH', '% MTD (VIP)'),
      ))
    if 'Doanh Số' in selected_metrics:
      # Chia /1.000.000 để hiển thị gọn (đơn vị triệu)
      def _ds_trieu(col):
        try:
          v = float(tot_row_s.get(col, 0) or 0) / 1_000_000
          return f'{v:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        except Exception:
          return '0'
      th_m = _ds_trieu('TH DS')
      ct_m = _ds_trieu('CT DS')
      pct = str(tot_row_s.get('% MTD DS', '0%'))
      if pct and not str(pct).endswith('%'):
        pct = f'{pct}%'
      cards.append(('Doanh Số (triệu)', f'{th_m}/{ct_m}/{pct}'))
    if 'PC BT' in selected_metrics:
      cards.append((
          'PC BT',
          _card_th_ct_pct('TH PC_BT', 'CT PC_BT', '% MTD PC_BT'),
      ))
    if 'LPPC' in selected_metrics:
      cards.append((
          'LPPC',
          _card_th_ct_pct('TH LPPC', 'CT LPPC', '% MTD LPPC', as_float=True),
      ))
    if 'ASO Trận Xanh' in selected_metrics:
      cards.append((
          'ASO Trận Xanh',
          _card_th_ct_pct('TH Xanh', 'CT Xanh', '% MTD Xanh'),
      ))
    if 'ASO Trận Vàng' in selected_metrics:
      cards.append((
          'ASO Trận Vàng',
          _card_th_ct_pct('TH Vàng', 'CT Vàng', '% MTD Vàng'),
      ))
    if 'PC Kênh ON' in selected_metrics:
      cards.append((
          'PC Kênh ON',
          _card_th_ct_pct('TH PC_ON', 'CT PC_ON', '% MTD PC_ON'),
      ))
    if 'KH Combo OFF' in selected_metrics:
      cards.append((
          'KH Combo OFF',
          _card_th_ct_pct('Đã Mua (OFF)', 'KH Combo OFF', '% MTD (OFF)'),
      ))
    if 'KH Combo ON' in selected_metrics:
      cards.append((
          'KH Combo ON',
          _card_th_ct_pct('Đã Mua (ON)', 'KH Combo ON', '% MTD (ON)'),
      ))
    if 'MBS Cat' in selected_metrics:
      cards.append((
          'MBS Cat',
          _card_th_ct_pct('Đã Mua (Cat)', 'MBS Cat', '% MTD (Cat)'),
      ))
    if 'MBS Brand' in selected_metrics:
      cards.append((
          'MBS Brand',
          _card_th_ct_pct('Đã Mua (Brand)', 'MBS Brand', '% MTD (Brand)'),
      ))

    if cards:
      # Hiển thị tối đa 4 card / hàng
      for start in range(0, len(cards), 4):
        row_cards = cards[start:start + 4]
        cols_m = st.columns(len(row_cards))
        for i, (lab, val) in enumerate(row_cards):
          with cols_m[i]:
            render_metric_card(lab, val)

    st.markdown(
        render_summary_html_table(df_summary, selected_metrics),
        unsafe_allow_html=True,
    )

    # ===== Chi tiết VIP MCH chưa mua hàng =====
    try:
      df_vip_chua = build_vip_mch_chua_mua(mcp, filter_nv=filter_nv, f_thu_list=f_thu_sum, df_cat=df_cat, df_brand=df_brand)
    except Exception as e:
      df_vip_chua = pd.DataFrame()
      st.caption(f'(Lỗi tải VIP chưa mua: {e})')

    st.markdown(
        '<p style="font-weight:800;color:#034ea2;margin:16px 0 6px;">'
        'CHI TIẾT NHÓM KH VIP MCH CHƯA MUA HÀNG</p>',
        unsafe_allow_html=True,
    )
    if df_vip_chua is None or df_vip_chua.empty:
      st.info('Không có cửa hàng VIP MCH nào chưa mua hàng theo bộ lọc hiện tại.')
    else:
      cols_vip = ['STT', 'Tên NVBH', 'Mã KH', 'Tên KH', 'VIP', 'Member Type', 'Thứ VT', 'Chỉ Tiêu', 'Trạng Thái']
      # Format giống bảng KPI (custom-kpi-table) + dòng Tổng Cộng
      _html = [
          '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">',
          '<table class="custom-kpi-table">',
          '<thead><tr>',
      ]
      for _c in cols_vip:
        _html.append(f'<th>{_c}</th>')
      _html.append('</tr></thead><tbody>')
      _sum_ct = 0.0
      for _i, (_, _row) in enumerate(df_vip_chua[cols_vip].iterrows()):
        _bg = '#e6f7ff' if _i % 2 == 0 else '#ffffff'
        _html.append(f'<tr style="background-color:{_bg} !important;">')
        for _c in cols_vip:
          _v = _row.get(_c, '')
          if pd.isna(_v):
            _v = ''
          if _c == 'Chỉ Tiêu':
            try:
              _num = float(_v) if _v != '' else 0.0
            except Exception:
              _num = 0.0
            _sum_ct += _num
            _s = format_number_vn(_num)
          else:
            _s = str(_v)
          if _c == 'Trạng Thái':
            _html.append(
                f'<td style="text-align:center;color:#c53030;font-weight:700;'
                f'background-color:{_bg} !important;">{_s}</td>'
            )
          elif _c in ('Tên NVBH', 'Tên KH'):
            _html.append(
                f'<td style="text-align:left;background-color:{_bg} !important;">{_s}</td>'
            )
          elif _c == 'Chỉ Tiêu':
            _html.append(
                f'<td style="text-align:right;background-color:{_bg} !important;">{_s}</td>'
            )
          else:
            _html.append(
                f'<td style="text-align:center;background-color:{_bg} !important;">{_s}</td>'
            )
        _html.append('</tr>')
      # Dòng Tổng Cộng — format giống total KPI (nền xanh đậm, chữ trắng)
      _tot_bg = '#1a365d'
      _html.append(f'<tr style="background-color:{_tot_bg} !important;">')
      for _c in cols_vip:
        if _c == 'STT':
          _s = ''
        elif _c == 'Tên NVBH':
          _s = 'TỔNG CỘNG'
        elif _c == 'Chỉ Tiêu':
          _s = format_number_vn(_sum_ct)
        elif _c == 'Trạng Thái':
          _s = f'{len(df_vip_chua)} CH'
        else:
          _s = ''
        _html.append(
            f'<td style="text-align:{"right" if _c == "Chỉ Tiêu" else "center"};'
            f'background-color:{_tot_bg} !important;color:#ffffff !important;'
            f'font-weight:800 !important;">{_s}</td>'
        )
      _html.append('</tr>')
      _html.append('</tbody></table></div>')
      st.markdown(''.join(_html), unsafe_allow_html=True)
      st.caption(f'Hiển thị: {len(df_vip_chua):,} cửa hàng VIP chưa mua hàng')
      st.download_button(
          '📥 Tải CSV VIP MCH chưa mua hàng',
          data=df_vip_chua.to_csv(index=False).encode('utf-8-sig'),
          file_name=f'VIP_MCH_ChuaMua_{report_date}.csv',
          mime='text/csv',
          key='dl_vip_mch_chua_mua',
      )


    # ===== Chart % hoàn thành KPI (theo metric đang chọn) =====
    try:
      import plotly.graph_objects as go
      chart_specs = [
          ('VIP MCH', 'VIP MCH', '% MTD (VIP)', 'Đã Mua (VIP)', 'VIP MCH'),
          ('Doanh Số', 'Doanh Số', '% MTD DS', 'TH DS', 'CT DS'),
          ('PC BT', 'PC BT', '% MTD PC_BT', 'TH PC_BT', 'CT PC_BT'),
          ('LPPC', 'LPPC', '% MTD LPPC', 'TH LPPC', 'CT LPPC'),
          ('ASO Trận Xanh', 'ASO Trận Xanh', '% MTD Xanh', 'TH Xanh', 'CT Xanh'),
          ('ASO Trận Vàng', 'ASO Trận Vàng', '% MTD Vàng', 'TH Vàng', 'CT Vàng'),
          ('PC Kênh ON', 'PC Kênh ON', '% MTD PC_ON', 'TH PC_ON', 'CT PC_ON'),
          ('KH Combo OFF', 'KH Combo OFF', '% MTD (OFF)', 'Đã Mua (OFF)', 'KH Combo OFF'),
          ('KH Combo ON', 'KH Combo ON', '% MTD (ON)', 'Đã Mua (ON)', 'KH Combo ON'),
          ('MBS Cat', 'MBS Cat', '% MTD (Cat)', 'Đã Mua (Cat)', 'MBS Cat'),
          ('MBS Brand', 'MBS Brand', '% MTD (Brand)', 'Đã Mua (Brand)', 'MBS Brand'),
      ]
      labels, pcts, hover = [], [], []
      for metric_key, label, pct_col, th_col, ct_col in chart_specs:
        if metric_key not in selected_metrics:
          continue
        try:
          raw = str(tot_row_s.get(pct_col, '0')).replace('%', '').strip()
          pct_v = float(raw) if raw else 0.0
        except Exception:
          pct_v = 0.0
        try:
          th_v = tot_row_s.get(th_col, 0)
          ct_v = tot_row_s.get(ct_col, 0)
        except Exception:
          th_v, ct_v = 0, 0
        labels.append(label)
        pcts.append(pct_v)
        hover.append(f'{label}<br>TH: {th_v}<br>CT: {ct_v}<br>%MTD: {pct_v}%')

      if labels:
        try:
          tg = float(st.session_state.get('timegone_pct', 0) or 0)
        except Exception:
          tg = 0.0
        # fallback timegone từ caption / global
        if not tg:
          try:
            from datetime import date as _d
            _rd = report_date if isinstance(report_date, _d) else pd.Timestamp(report_date).date()
            _, _, _, tg = get_timegone_stats(_rd)
            tg = float(tg or 0)
          except Exception:
            tg = 0.0
        # Palette tương phản — mỗi KPI 1 màu, không lặp
        _PALETTE = [
            '#e53e3e', '#3182ce', '#38a169', '#dd6b20',
            '#805ad5', '#d69e2e', '#319795', '#d53f8c',
            '#2b6cb0', '#c05621', '#276749', '#6b46c1',
        ]
        colors = [_PALETTE[i % len(_PALETTE)] for i in range(len(pcts))]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=labels,
            y=pcts,
            text=[f'{p}%' for p in pcts],
            textposition='outside',
            marker_color=colors,
            hovertext=hover,
            hoverinfo='text',
            name='% MTD',
        ))
        if tg > 0:
          fig.add_hline(
              y=tg, line_dash='dash', line_color='#3182ce', line_width=2,
              annotation_text=f'Timegone {tg:.0f}%', annotation_position='top right',
          )
        fig.add_hline(
            y=100, line_dash='dot', line_color='#718096', line_width=1,
            annotation_text='100%', annotation_position='top left',
        )
        fig.update_layout(
            title=dict(
                text='Mức độ hoàn thành KPI / Chỉ tiêu (% MTD)',
                font=dict(size=15, color='#1a365d', family='Arial'),
                x=0.5, xanchor='center',
            ),
            yaxis=dict(
                title='% MTD',
                range=[0, max(120, (max(pcts) + 15) if pcts else 120)],
                ticksuffix='%', gridcolor='#e2e8f0',
            ),
            xaxis=dict(tickangle=-25, tickfont=dict(size=11)),
            margin=dict(l=40, r=20, t=50, b=80),
            height=380,
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            bargap=0.35,
        )
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        })
    except Exception as _e_chart:
      st.caption(f'Không vẽ được chart KPI: {_e_chart}')

    st.markdown(
        f"""
        <div class="note-box">
            <div style="font-weight: 800; color: #034ea2; margin-bottom: 8px; font-size: 13.5px;">NHẬN XÉT & ĐÁNH GIÁ BÁO CÁO TỔNG HỢP:</div>
            <ul style="margin: 0; padding-left: 18px; line-height: 1.6;">
                <li><b>Kết Quả Tổng Quan:</b> Tổng số lượng cửa hàng VIP (VIP3, VIP5, VIPSI) toàn đội đạt <b>{tot_row_s['VIP MCH']:,} cửa hàng</b> (Đã mua: {tot_row_s['Đã Mua (VIP)']:,}).</li>
                <li><b>Chương Trình Combo & MBS:</b> Tổng KH tham gia Combo OFF: <b>{tot_row_s['KH Combo OFF']:,} CH</b> (Đã mua: {tot_row_s['Đã Mua (OFF)']:,}) | Combo ON: <b>{tot_row_s['KH Combo ON']:,} CH</b> (Đã mua: {tot_row_s['Đã Mua (ON)']:,}). MBS Category: <b>{tot_row_s['MBS Cat']:,} CH</b> | MBS Brand: <b>{tot_row_s['MBS Brand']:,} CH</b>.</li>
                <li><b>Đề Xuất Hành Động:</b> Tiếp tục bám sát lịch tuyến, đẩy mạnh các nhóm cửa hàng chưa phát sinh và đôn đốc các ĐDKD hoàn thành toàn diện các chỉ tiêu trong tháng {report_date.strftime('%m/%Y')}.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )



  elif selected_kpi == 'MBS_CAT':
    set_color_moc_for_kpi('MBS_CAT')
    result = build_mbs_cat_report(df_cat, filter_nv, mcp_df=mcp)
    groups = result['groups']
    df_detail = result['df_detail']
    total_kh = result['total_kh']

    st.markdown(
        f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 4px;'
        f' font-size: 16px; text-align: center;">BÁO CÁO TỔNG HỢP MBS CAT'
        f' - 6 NHÓM</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="text-align: center; font-size: 12px; color: #4a5568;'
        f' margin-bottom: 8px;">Tổng Doanh Số thực đạt / Chỉ tiêu từng KH'
        f' | Lọc NV: {nv_label(filter_nv)} | Tổng KH MBS: <b>{total_kh}</b></p>',
        unsafe_allow_html=True,
    )

    # Áp dụng lọc Thứ VT (từ bộ lọc chính phía trên) lên df_detail + tính lại 6 nhóm
    f_thu_vt = f_thu_vt_main if selected_kpi == 'MBS_CAT' else []
    if total_kh > 0 and f_thu_vt and 'Thứ VT' in df_detail.columns:
      thu_s = df_detail['Thứ VT'].astype(str).str.strip()
      mapping_rules = {
          '2': ['2', '25'], '3': ['3', '36'], '4': ['4', '47'],
          '5': ['5', '25'], '6': ['6', '36'], '7': ['7', '47'],
          '25': ['25'], '36': ['36'], '47': ['47'],
      }
      mask = pd.Series(False, index=df_detail.index)
      for t in f_thu_vt:
        valid_set = mapping_rules.get(str(t).strip(), [str(t).strip()])
        mask = mask | thu_s.isin(valid_set)
      df_detail = df_detail[mask].copy()
      total_kh = len(df_detail)
      # Tính lại groups
      group_meta = {
          1: ('Nhóm 1 · Đã đạt MBS', '#c6f6d5', '#22543d'),
          2: ('Nhóm 2 · Đạt DS, thiếu nhiệm vụ', '#edf2f7', '#2d3748'),
          3: ('Nhóm 3 · Đạt nhiệm vụ, DS ≥50% Target', '#edf2f7', '#2d3748'),
          4: ('Nhóm 4 · DS ≥60% Target, thiếu nhiệm vụ', '#e6fffa', '#234e52'),
          5: ('Nhóm 5 · Chưa phát sinh DS', '#fff5f5', '#c53030'),
          6: ('Nhóm 6 · Còn lại', '#ebf8ff', '#2b6cb0'),
      }
      groups = {}
      for g in range(1, 7):
        sub = df_detail[df_detail['Nhóm'] == g]
        kh = len(sub)
        act = float(sub['Actual'].sum()) if kh else 0.0
        tgt = float(sub['Target'].sum()) if kh else 0.0
        pct_th = round(act / tgt * 100, 1) if tgt > 0 else 0.0
        pct_kh = round(kh / total_kh * 100, 1) if total_kh else 0.0
        name, bg, color = group_meta[g]
        groups[g] = {
            'name': name, 'kh': kh, 'total_kh': total_kh,
            'pct_kh': pct_kh, 'actual': act, 'target': tgt,
            'pct_th': pct_th, 'bg': bg, 'color': color,
        }

    if total_kh == 0:
      st.warning('Không có dữ liệu Data_Cat để chạy báo cáo MBS CAT.')
    else:
      # 6 cards - grid responsive (3 cột desktop / 2 cột mobile / 1 cột máy nhỏ)
      cards_html = ['<div class="mbs-card-grid">']
      for g in [1, 2, 3, 4, 5, 6]:
        ginfo = groups[g]
        pct_badge_bg = (
            '#c6f6d5'
            if ginfo['pct_th'] >= 70
            else ('#fefcbf' if ginfo['pct_th'] >= 50 else '#fed7d7')
        )
        pct_badge_color = (
            '#22543d'
            if ginfo['pct_th'] >= 70
            else ('#744210' if ginfo['pct_th'] >= 50 else '#c53030')
        )
        cards_html.append(
            '<div class="mbs-card" style="background:' + ginfo['bg'] + ';">'
            '<div class="mbs-card-title" style="color:' + ginfo['color'] + ';">'
            + ginfo['name'] + '</div>'
            '<div class="mbs-card-kh" style="color:' + ginfo['color'] + ';">'
            + str(ginfo['kh']) + ' KH'
            '<span> / ' + str(ginfo['total_kh']) + ' KH</span></div>'
            '<div class="mbs-card-pct">' + str(ginfo['pct_kh'])
            + '% tổng KH MBS</div>'
            '<div class="mbs-card-footer">'
            'Actual <b>' + format_trieu(ginfo['actual']) + '</b>'
            ' / Target <b>' + format_trieu(ginfo['target']) + '</b> Tr'
            ' / % TH '
            '<span style="background:' + pct_badge_bg + '; color:' + pct_badge_color + ';'
            ' font-weight:800; padding:1px 6px; border-radius:8px;">'
            + str(ginfo['pct_th']) + '%</span></div></div>'
        )
      cards_html.append('</div>')
      st.markdown(''.join(cards_html), unsafe_allow_html=True)

      st.markdown(
          '<p style="font-weight:800; color:#034ea2; margin:12px 0 6px 0;">'
          '📋 CHI TIẾT TỪNG KHÁCH HÀNG THEO NHÓM</p>',
          unsafe_allow_html=True,
      )

      # Lọc nhóm (popover) — Thứ VT đã nằm phía trên 6 nhóm
      st.markdown(
          """
          <style>
          div[data-testid="stPopover"] button {
            font-size: 12px !important;
            padding: 0.35rem 0.8rem !important;
            min-height: 2.4rem !important;
            width: 100% !important;
            justify-content: center !important;
          }
          </style>
          """,
          unsafe_allow_html=True,
      )
      fc1, _ = st.columns([1, 3])
      with fc1:
        st.markdown(
            '<p class="filter-label" style="margin-bottom:2px;font-size:11px !important;">'
            '👁️ Lọc nhóm</p>',
            unsafe_allow_html=True,
        )
        with st.popover('Chọn nhóm hiển thị', use_container_width=True):
          nhom_filter = st.multiselect(
              '',
              options=[1, 2, 3, 4, 5, 6],
              default=[1, 2, 3, 4, 5, 6],
              format_func=lambda x: groups[x]['name'],
              key='mbs_cat_nhom_filter',
              label_visibility='collapsed',
          )

      nhom_selected = st.session_state.get(
          'mbs_cat_nhom_filter', [1, 2, 3, 4, 5, 6]
      )
      if not nhom_selected:
        nhom_selected = [1, 2, 3, 4, 5, 6]

      # Bộ lọc CAT + Đạt Nhiệm Vụ
      cat_opts = sorted([
          str(x).strip() for x in df_detail.get('Member type', pd.Series(dtype=str)).dropna().unique()
          if str(x).strip() and str(x).strip().lower() not in ('nan', 'none')
      ]) if 'Member type' in df_detail.columns else []
      fc_a, fc_b = st.columns(2)
      with fc_a:
        st.markdown(
            '<p class="filter-label" style="margin-bottom:2px;font-size:11px !important;">'
            '🏷️ Lọc CAT</p>',
            unsafe_allow_html=True,
        )
        member_selected = st.multiselect(
            '', options=cat_opts, default=[],
            key='mbs_cat_member_filter', placeholder='Tất cả CAT',
            label_visibility='collapsed',
        )
      with fc_b:
        st.markdown(
            '<p class="filter-label" style="margin-bottom:2px;font-size:11px !important;">'
            '✅ Đạt Nhiệm Vụ</p>',
            unsafe_allow_html=True,
        )
        mission_selected = st.multiselect(
            '', options=['Có', 'Không'], default=[],
            key='mbs_cat_mission_filter', placeholder='Tất cả',
            label_visibility='collapsed',
        )

      df_show = df_detail[df_detail['Nhóm'].isin(nhom_selected)].copy()
      if member_selected and 'Member type' in df_show.columns:
        df_show = df_show[df_show['Member type'].astype(str).str.strip().isin(member_selected)]
      if mission_selected and 'Đạt nhiệm vụ' in df_show.columns:
        df_show = df_show[df_show['Đạt nhiệm vụ'].astype(str).str.strip().isin(mission_selected)]

      if not df_show.empty:
        df_show = df_show.sort_values(
            ['Nhóm', 'Actual'], ascending=[True, False]
        ).reset_index(drop=True)
        df_show.insert(0, 'STT', range(1, len(df_show) + 1))
        def _fmt_num(x):
          try:
            return f'{float(x):,.0f}'.replace(',', '.')
          except Exception:
            return x
        df_show['Actual'] = df_show['Actual'].apply(_fmt_num)
        if 'Actual (Not Cancel/Pending)' in df_show.columns:
          df_show['Actual (Not Cancel/Pending)'] = df_show[
              'Actual (Not Cancel/Pending)'
          ].apply(_fmt_num)
        df_show['Target'] = df_show['Target'].apply(_fmt_num)
        def _fmt_pct(x):
          try:
            return f"{float(str(x).replace('%','')):.1f}%"
          except Exception:
            return '0%'
        df_show['% TH'] = df_show['% TH'].apply(_fmt_pct)
        cols_show = [
            'STT',
            'Tên nhóm',
            'Outlet Code',
            'Tên CH',
            'Tên NVBH',
            'Thứ VT',
            'Member type',
            'Actual',
            'Actual (Not Cancel/Pending)',
            'Target',
            '% TH',
            'Đạt nhiệm vụ',
        ]
        df_html = df_show[[c for c in cols_show if c in df_show.columns]].copy()
        st.markdown(render_html_table(df_html), unsafe_allow_html=True)
        st.caption(f'Hiển thị: {len(df_show):,} / {total_kh:,} KH')
        render_mbs_pie_chart(df_show, title='Tỷ lệ KH theo Nhóm — MBS CAT')
        st.download_button(
            label='⬇️ Xuất file CSV - Chi tiết MBS CAT',
            data=df_html.to_csv(index=False).encode('utf-8-sig'),
            file_name='MBS_CAT_ChiTiet_KH.csv',
            mime='text/csv',
            key='mbs_cat_export_csv',
        )
      else:
        st.info('Không có KH phù hợp bộ lọc hiện tại.')

      g1, g5 = groups[1], groups[5]
      note_html = (
          '<div class="note-box">'
          '<div style="font-weight:800; color:#034ea2; margin-bottom:8px;'
          ' font-size:13.5px;">NHẬN XÉT & ĐÁNH GIÁ MBS CAT:</div>'
          '<ul style="margin:0; padding-left:18px; line-height:1.6;">'
          '<li><b>Đã đạt MBS (Nhóm 1):</b> ' + str(g1['kh']) + ' KH ('
          + str(g1['pct_kh']) + '% tổng) — Actual '
          + format_trieu(g1['actual']) + ' Tr / Target '
          + format_trieu(g1['target']) + ' Tr (' + str(g1['pct_th'])
          + '% TH).</li>'
          '<li><b>Chưa phát sinh DS (Nhóm 5):</b> ' + str(g5['kh'])
          + ' KH (' + str(g5['pct_kh'])
          + '%) — cần đôn đốc mở đơn ngay.</li>'
          '<li><b>Đề xuất:</b> Ưu tiên đẩy nhiệm vụ Cat NEW ≥ 200.000 cho'
          ' Nhóm 2 &amp; 4 (đã có DS nhưng thiếu nhiệm vụ); kích hoạt'
          ' Nhóm 5 chưa phát sinh.</li>'
          '</ul></div>'
      )
      st.markdown(note_html, unsafe_allow_html=True)


  elif selected_kpi == 'MBS_BRAND':
    set_color_moc_for_kpi('MBS_BRAND')
    result = build_mbs_brand_report(df_brand, filter_nv, mcp_df=mcp)
    groups = result['groups']
    df_detail = result['df_detail']
    total_kh = result['total_kh']

    st.markdown(
        f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 4px;'
        f' font-size: 16px; text-align: center;">BÁO CÁO TỔNG HỢP MBS BRAND'
        f' - 6 NHÓM</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="text-align: center; font-size: 12px; color: #4a5568;'
        f' margin-bottom: 8px;">Tổng Doanh Số thực đạt / Chỉ tiêu từng KH'
        f' | Lọc NV: {nv_label(filter_nv)} | Tổng KH MBS: <b>{total_kh}</b></p>',
        unsafe_allow_html=True,
    )

    f_thu_vt = f_thu_vt_main if selected_kpi == 'MBS_BRAND' else []
    if total_kh > 0 and f_thu_vt and 'Thứ VT' in df_detail.columns:
      thu_s = df_detail['Thứ VT'].astype(str).str.strip()
      mapping_rules = {
          '2': ['2', '25'], '3': ['3', '36'], '4': ['4', '47'],
          '5': ['5', '25'], '6': ['6', '36'], '7': ['7', '47'],
          '25': ['25'], '36': ['36'], '47': ['47'],
      }
      mask = pd.Series(False, index=df_detail.index)
      for t in f_thu_vt:
        valid_set = mapping_rules.get(str(t).strip(), [str(t).strip()])
        mask = mask | thu_s.isin(valid_set)
      df_detail = df_detail[mask].copy()
      total_kh = len(df_detail)
      group_meta = {
          1: ('Nhóm 1 · Đã đạt MBS', '#c6f6d5', '#22543d'),
          2: ('Nhóm 2 · Đạt DS, thiếu nhiệm vụ', '#edf2f7', '#2d3748'),
          3: ('Nhóm 3 · Đạt nhiệm vụ, DS ≥50% Target', '#edf2f7', '#2d3748'),
          4: ('Nhóm 4 · DS ≥60% Target, thiếu nhiệm vụ', '#e6fffa', '#234e52'),
          5: ('Nhóm 5 · Chưa phát sinh DS', '#fff5f5', '#c53030'),
          6: ('Nhóm 6 · Còn lại', '#ebf8ff', '#2b6cb0'),
      }
      groups = {}
      for g in range(1, 7):
        sub = df_detail[df_detail['Nhóm'] == g]
        kh = len(sub)
        act = float(sub['Actual'].sum()) if kh else 0.0
        tgt = float(sub['Target'].sum()) if kh else 0.0
        pct_th = round(act / tgt * 100, 1) if tgt > 0 else 0.0
        pct_kh = round(kh / total_kh * 100, 1) if total_kh else 0.0
        name, bg, color = group_meta[g]
        groups[g] = {
            'name': name, 'kh': kh, 'total_kh': total_kh,
            'pct_kh': pct_kh, 'actual': act, 'target': tgt,
            'pct_th': pct_th, 'bg': bg, 'color': color,
        }

    if total_kh == 0:
      st.warning('Không có dữ liệu Data_Brand để chạy báo cáo MBS BRAND.')
    else:
      # 6 cards - grid responsive (3 cột desktop / 2 cột mobile / 1 cột máy nhỏ)
      cards_html = ['<div class="mbs-card-grid">']
      for g in [1, 2, 3, 4, 5, 6]:
        ginfo = groups[g]
        pct_badge_bg = (
            '#c6f6d5'
            if ginfo['pct_th'] >= 70
            else ('#fefcbf' if ginfo['pct_th'] >= 50 else '#fed7d7')
        )
        pct_badge_color = (
            '#22543d'
            if ginfo['pct_th'] >= 70
            else ('#744210' if ginfo['pct_th'] >= 50 else '#c53030')
        )
        cards_html.append(
            '<div class="mbs-card" style="background:' + ginfo['bg'] + ';">'
            '<div class="mbs-card-title" style="color:' + ginfo['color'] + ';">'
            + ginfo['name'] + '</div>'
            '<div class="mbs-card-kh" style="color:' + ginfo['color'] + ';">'
            + str(ginfo['kh']) + ' KH'
            '<span> / ' + str(ginfo['total_kh']) + ' KH</span></div>'
            '<div class="mbs-card-pct">' + str(ginfo['pct_kh'])
            + '% tổng KH MBS</div>'
            '<div class="mbs-card-footer">'
            'Actual <b>' + format_trieu(ginfo['actual']) + '</b>'
            ' / Target <b>' + format_trieu(ginfo['target']) + '</b> Tr'
            ' / % TH '
            '<span style="background:' + pct_badge_bg + '; color:' + pct_badge_color + ';'
            ' font-weight:800; padding:1px 6px; border-radius:8px;">'
            + str(ginfo['pct_th']) + '%</span></div></div>'
        )
      cards_html.append('</div>')
      st.markdown(''.join(cards_html), unsafe_allow_html=True)

      st.markdown(
          '<p style="font-weight:800; color:#034ea2; margin:12px 0 6px 0;">'
          '📋 CHI TIẾT TỪNG KHÁCH HÀNG THEO NHÓM (BRAND)</p>',
          unsafe_allow_html=True,
      )
      st.markdown(
          """
          <style>
          div[data-testid="stPopover"] button {
            font-size: 12px !important;
            padding: 0.35rem 0.8rem !important;
            min-height: 2.4rem !important;
            width: 100% !important;
            justify-content: center !important;
          }
          </style>
          """,
          unsafe_allow_html=True,
      )
      fc1, _ = st.columns([1, 3])
      with fc1:
        st.markdown(
            '<p class="filter-label" style="margin-bottom:2px;font-size:11px !important;">'
            '👁️ Lọc nhóm</p>',
            unsafe_allow_html=True,
        )
        with st.popover('Chọn nhóm hiển thị', use_container_width=True):
          st.multiselect(
              '',
              options=[1, 2, 3, 4, 5, 6],
              default=[1, 2, 3, 4, 5, 6],
              format_func=lambda x: groups[x]['name'],
              key='mbs_brand_nhom_filter',
              label_visibility='collapsed',
          )

      nhom_selected = st.session_state.get(
          'mbs_brand_nhom_filter', [1, 2, 3, 4, 5, 6]
      )
      if not nhom_selected:
        nhom_selected = [1, 2, 3, 4, 5, 6]

      brand_opts = sorted([
          str(x).strip() for x in df_detail.get('Member type', pd.Series(dtype=str)).dropna().unique()
          if str(x).strip() and str(x).strip().lower() not in ('nan', 'none')
      ]) if 'Member type' in df_detail.columns else []
      fb_a, fb_b = st.columns(2)
      with fb_a:
        st.markdown(
            '<p class="filter-label" style="margin-bottom:2px;font-size:11px !important;">'
            '🏷️ Lọc BRAND</p>',
            unsafe_allow_html=True,
        )
        member_selected_b = st.multiselect(
            '', options=brand_opts, default=[],
            key='mbs_brand_member_filter', placeholder='Tất cả BRAND',
            label_visibility='collapsed',
        )
      with fb_b:
        st.markdown(
            '<p class="filter-label" style="margin-bottom:2px;font-size:11px !important;">'
            '✅ Đạt Nhiệm Vụ</p>',
            unsafe_allow_html=True,
        )
        mission_selected_b = st.multiselect(
            '', options=['Có', 'Không'], default=[],
            key='mbs_brand_mission_filter', placeholder='Tất cả',
            label_visibility='collapsed',
        )

      df_show = df_detail[df_detail['Nhóm'].isin(nhom_selected)].copy()
      if member_selected_b and 'Member type' in df_show.columns:
        df_show = df_show[df_show['Member type'].astype(str).str.strip().isin(member_selected_b)]
      if mission_selected_b and 'Đạt nhiệm vụ' in df_show.columns:
        df_show = df_show[df_show['Đạt nhiệm vụ'].astype(str).str.strip().isin(mission_selected_b)]

      if not df_show.empty:
        df_show = df_show.sort_values(
            ['Nhóm', 'Actual'], ascending=[True, False]
        ).reset_index(drop=True)
        df_show.insert(0, 'STT', range(1, len(df_show) + 1))
        def _fmt_num_b(x):
          try:
            return f'{float(x):,.0f}'.replace(',', '.')
          except Exception:
            return x
        df_show['Actual'] = df_show['Actual'].apply(_fmt_num_b)
        if 'Actual (Not Cancel/Pending)' in df_show.columns:
          df_show['Actual (Not Cancel/Pending)'] = df_show[
              'Actual (Not Cancel/Pending)'
          ].apply(_fmt_num_b)
        df_show['Target'] = df_show['Target'].apply(_fmt_num_b)
        def _fmt_pct_brand(x):
          try:
            return f"{float(str(x).replace('%','')):.1f}%"
          except Exception:
            return '0%'
        df_show['% TH'] = df_show['% TH'].apply(_fmt_pct_brand)
        cols_show = [
            'STT', 'Tên nhóm', 'Outlet Code', 'Tên CH', 'Tên NVBH',
            'Thứ VT', 'Member type', 'Actual',
            'Actual (Not Cancel/Pending)', 'Target', '% TH',
            'Đạt nhiệm vụ',
        ]
        df_html = df_show[[c for c in cols_show if c in df_show.columns]].copy()
        st.markdown(render_html_table(df_html), unsafe_allow_html=True)
        st.caption(f'Hiển thị: {len(df_show):,} / {total_kh:,} KH')
        render_mbs_pie_chart(df_show, title='Tỷ lệ KH theo Nhóm — MBS BRAND')
        st.download_button(
            label='⬇️ Xuất file CSV - Chi tiết MBS BRAND',
            data=df_html.to_csv(index=False).encode('utf-8-sig'),
            file_name='MBS_BRAND_ChiTiet_KH.csv',
            mime='text/csv',
            key='mbs_brand_export_csv',
        )
      else:
        st.info('Không có KH phù hợp bộ lọc hiện tại.')

      g1, g5 = groups[1], groups[5]
      note_html = (
          '<div class="note-box">'
          '<div style="font-weight:800; color:#034ea2; margin-bottom:8px;'
          ' font-size:13.5px;">NHẬN XÉT & ĐÁNH GIÁ MBS BRAND:</div>'
          '<ul style="margin:0; padding-left:18px; line-height:1.6;">'
          '<li><b>Đã đạt MBS (Nhóm 1):</b> ' + str(g1['kh']) + ' KH ('
          + str(g1['pct_kh']) + '% tổng) — Actual '
          + format_trieu(g1['actual']) + ' Tr / Target '
          + format_trieu(g1['target']) + ' Tr (' + str(g1['pct_th'])
          + '% TH).</li>'
          '<li><b>Chưa phát sinh DS (Nhóm 5):</b> ' + str(g5['kh'])
          + ' KH (' + str(g5['pct_kh'])
          + '%) — cần đôn đốc mở đơn ngay.</li>'
          '<li><b>Đề xuất:</b> Ưu tiên đẩy nhiệm vụ Brand NEW ≥ 200.000 cho'
          ' Nhóm 2 &amp; 4; kích hoạt Nhóm 5 chưa phát sinh.</li>'
          '</ul></div>'
      )
      st.markdown(note_html, unsafe_allow_html=True)


  elif selected_kpi == 'VISIT':
    set_color_moc_for_kpi('VISIT')
    # ===== TỰ NHẬN THỨ + TUẦN ISO CHẴN/LẺ TỪ NGÀY CHỌN =====
    iso_year, iso_week, iso_weekday = report_date.isocalendar()
    week_type = 'Tuần Chẵn' if iso_week % 2 == 0 else 'Tuần Lẻ'
    wday = report_date.weekday()  # 0=Mon ... 6=Sun

    weekday_map = {
        0: 'THỨ HAI',
        1: 'THỨ BA',
        2: 'THỨ TƯ',
        3: 'THỨ NĂM',
        4: 'THỨ SÁU',
        5: 'THỨ BẢY',
        6: 'CHỦ NHẬT',
    }
    wname = weekday_map.get(wday, '')

    # Map thứ → mã chu kỳ viếng thăm tương ứng
    # Thứ 2/5 → 2 + 25 | Thứ 3/6 → 3 + 36 | Thứ 4/7 → 4 + 47
    auto_thu_map = {
        0: ['2', '25'],   # Thứ 2
        1: ['3', '36'],   # Thứ 3
        2: ['4', '47'],   # Thứ 4
        3: ['5', '25'],   # Thứ 5
        4: ['6', '36'],   # Thứ 6
        5: ['7', '47'],   # Thứ 7
        6: [],            # Chủ nhật
    }
    auto_thu = auto_thu_map.get(wday, [])

    # Khi đổi NGÀY → tự reset filter theo thứ của ngày đó
    date_key = report_date.strftime('%Y-%m-%d')
    if st.session_state.get('visit_last_date') != date_key:
      st.session_state['visit_last_date'] = date_key
      st.session_state['visit_thu_input'] = auto_thu
      st.query_params['visit_thu'] = ','.join(auto_thu)

    saved_visit_thu = st.query_params.get('visit_thu', '')
    default_visit_thu_list = (
        [x.strip() for x in saved_visit_thu.split(',') if x.strip()]
        if saved_visit_thu
        else auto_thu
    )

    def update_visit_params():
      st.query_params['visit_thu'] = (
          ','.join(st.session_state.visit_thu_input)
          if st.session_state.visit_thu_input
          else ''
      )

    st.markdown(
        '<p class="filter-label">📅 Lọc Theo Thứ / Chu kỳ Viếng Thăm (Chọn'
        ' nhiều)</p>',
        unsafe_allow_html=True,
    )
    thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
    valid_visit_thu = [t for t in default_visit_thu_list if t in thu_opts]
    f_thu_visit = st.multiselect(
        '',
        thu_opts,
        default=valid_visit_thu,
        key='visit_thu_input',
        on_change=update_visit_params,
        label_visibility='collapsed',
    )

    st.query_params['visit_thu'] = (
        ','.join(st.session_state.visit_thu_input)
        if st.session_state.visit_thu_input
        else ''
    )

    (
        df_visit,
        v3_m,
        v3_t,
        v5_m,
        v5_t,
        vsi_m,
        vsi_t,
        le_m,
        le_t,
        on_m,
        on_t,
        title_v,
    ) = build_visit_report(mcp, df, report_date, filter_nv, f_thu_visit)

    st.markdown(
        f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 2px;'
        f' font-size: 16px; text-align: center;">BÁO CÁO LỊCH VIẾNG THĂM & % ACTIVE'
        f' {wname} ({week_type} - Tuần {iso_week}) - {report_date.strftime("%d/%m/%Y")}</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="text-align: center; font-size: 12px; color: #4a5568;'
        f' margin-bottom: 12px;">Dữ liệu cập nhật {wname} ngày'
        f' {report_date.strftime("%d/%m/%Y")} | {week_type} (ISO tuần {iso_week}/{iso_year})'
        f' | Kèm tỷ lệ % Active (Đã mua / Tổng KH)</p>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
      p3 = round(v3_m / v3_t * 100, 1) if v3_t else 0
      render_metric_card('VIP 3', f'{v3_m} / {v3_t} ({p3}%)')
    with c2:
      p5 = round(v5_m / v5_t * 100, 1) if v5_t else 0
      render_metric_card('VIP 5', f'{v5_m} / {v5_t} ({p5}%)')
    with c3:
      psi = round(vsi_m / vsi_t * 100, 1) if vsi_t else 0
      render_metric_card('VIPSI', f'{vsi_m} / {vsi_t} ({psi}%)')
    with c4:
      ple = round(le_m / le_t * 100, 1) if le_t else 0
      render_metric_card('LẺ', f'{le_m} / {le_t} ({ple}%)')
    with c5:
      pon = round(on_m / on_t * 100, 1) if on_t else 0
      render_metric_card('ON', f'{on_m} / {on_t} ({pon}%)')

    st.markdown(render_visit_html_table(df_visit), unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="note-box">
            <div style="font-weight: 800; color: #034ea2; margin-bottom: 8px; font-size: 13.5px;">NHẬN XÉT & ĐÁNH GIÁ LỊCH VIẾNG THĂM {wname} ({week_type} - Tuần {iso_week}):</div>
            <ul style="margin: 0; padding-left: 18px; line-height: 1.6;">
                <li><b>Kết Quả Thực Hiện:</b> Theo dõi sát sao tỷ lệ mua hàng thực tế (Active) so với lịch tuyến viếng thăm trong ngày {report_date.strftime('%d/%m/%Y')}.</li>
                <li><b>Trọng Tâm Vận Hành:</b> Ưu tiên bám sát các nhóm cửa hàng VIP và Kênh ON Premise để đảm bảo đạt chuẩn bao phủ và tối ưu sản lượng.</li>
                <li><b>Đề Xuất Hành Động:</b> SS đồng hành cùng các ĐDKD đi thị trường (Field Coaching) trực tiếp tại các tuyến có tỷ lệ active chưa đạt yêu cầu.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

  elif selected_kpi == 'TURNOVER':
    set_color_moc_for_kpi('TURNOVER')
    df_r, team_tgt, title = build_turnover_report(
        df, report_date, turnover_targets, filter_nv
    )
    if df_r is None or df_r.empty:
      st.warning('Không có dữ liệu TURNOVER.')
      st.stop()
    total_row = df_r.iloc[-1]
    total_mtd = float(total_row['Doanh Số MTD'])
    total_today = float(total_row['Thực Hiện Ngày'])
    pct_team = total_row['% MTD']

    st.markdown(
        f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px;'
        f' font-size: 16px; text-align: center;">{title} - THÁNG'
        f' {report_date.strftime("%m/%Y")}</h3>',
        unsafe_allow_html=True,
    )
    st.caption(
        f"⚡ Ngày: {report_date.strftime('%d/%m/%Y')} | Lọc: {nv_label(filter_nv)}"
    )
    st.markdown(
        f'<div style="text-align:center; font-size:12px; color:#7a1f1f; font-weight:700; margin:2px 0 8px;">💰 Mức lương KPI: {KPI_SALARY_LABEL.get("TURNOVER", "")}</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
      render_metric_card(
          '🎯 Chỉ Tiêu DS', f"{team_tgt:,.0f}".replace(',', '.')
      )
    with c2:
      render_metric_card(
          '📈 Doanh Số MTD', f"{total_mtd:,.0f}".replace(',', '.')
      )
    with c3:
      render_metric_card('📊 % MTD', pct_team)
    with c4:
      render_metric_card(
          '🆕 Thực Hiện Ngày', f"{total_today:,.0f}".replace(',', '.')
      )

    df_display = df_r.copy()
    for col in ['Chỉ Tiêu Doanh Số', 'Thực Hiện Ngày', 'Doanh Số MTD', 'GAP']:
      if col in df_display.columns:
        df_display[col] = df_display[col].apply(
            lambda x: f'{x:,.0f}'.replace(',', '.')
            if isinstance(x, (int, float))
            else x
        )
    if 'Bình quân ngày' in df_display.columns:
      df_display['Bình quân ngày'] = df_display['Bình quân ngày'].apply(
          lambda x: f'{x:,.1f}'.replace(',', '.')
          if isinstance(x, (int, float))
          else x
      )

    st.markdown(render_html_table(df_display), unsafe_allow_html=True)

    df_eval = df_r.iloc[:-1].copy()
    df_eval['_pct_val'] = (
        df_eval['% MTD'].str.replace('%', '').astype(float)
    )
    df_sorted_pct = df_eval.sort_values(by='_pct_val', ascending=False)
    top3 = df_sorted_pct.head(3)
    bottom3 = df_sorted_pct.tail(3).iloc[::-1]

    top3_text = ', '.join(
        [f"{r['Tên NVBH']} ({r['% MTD']})" for _, r in top3.iterrows()]
    )
    bottom3_text = ', '.join(
        [f"{r['Tên NVBH']} ({r['% MTD']})" for _, r in bottom3.iterrows()]
    )

    st.markdown(
        f"""
        <div class="note-box">
            <div style="font-weight: 800; color: #034ea2; margin-bottom: 8px; font-size: 13.5px;">NHẬN XÉT & ĐÁNH GIÁ {title}:</div>
            <ul style="margin: 0; padding-left: 18px; line-height: 1.6;">
                <li><b>Kết Quả Thực Hiện:</b> Đạt {total_mtd:,.0f} / {team_tgt:,.0f} VNĐ ({pct_team} MTD). Thực hiện ngày: {total_today:,.0f} VNĐ.</li>
                <li><b>Top 3 ĐDKD Dẫn Đầu:</b> {top3_text}.</li>
                <li><b>Bottom 3 ĐDKD Cần Cải Thiện:</b> {bottom3_text}.</li>
                <li><b>Đề Xuất Hành Động Cho 3 Bạn Bottom:</b> Tập trung rà soát doanh số khách hàng trọng điểm, thúc đẩy đơn hàng lớn và SS hỗ trợ trực tiếp tại tuyến.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

  elif selected_kpi == 'PERFORMANCE':
    set_color_moc_for_kpi('SUMMARY')
    if df_visit_sched is None or df_visit_sched.empty:
      st.warning(
          '⚠️ Chưa có file **DanhSachLichViengTham.xlsx** trong thư mục `data/`. '
          'Upload file lịch viếng thăm lên GitHub rồi bấm **Xóa Cache & Reload**.'
      )
    else:
      df_perf, title_perf = build_performance_report(
          df, mcp, df_visit_sched, report_date, turnover_targets, filter_nv
      )
      st.markdown(
          f'<h3 style="color:#034ea2;font-weight:800;text-align:center;">'
          f'{title_perf} - {report_date.strftime("%d/%m/%Y")}</h3>',
          unsafe_allow_html=True,
      )
      st.caption(
          '⚡ Nguồn: DanhSachLichViengTham + RPT + MCP | '
          f'Lọc: {nv_label(filter_nv)} | Giữa ngày < 13h | PC = CH có đơn (không MOQ)'
      )
      if df_perf is None or df_perf.empty:
        st.info('Không có dữ liệu hiệu suất cho ngày này.')
      else:
        st.markdown(render_performance_html(df_perf), unsafe_allow_html=True)
        # Chi tiết ĐH Trái Tuyến phía dưới 2 bảng
        df_trai = build_trai_tuyen_orders(
            df, df_visit_sched, mcp, report_date, filter_nv
        )
        st.markdown(render_trai_tuyen_html(df_trai), unsafe_allow_html=True)
        # Chi tiết VIP KO ĐH phía dưới ĐH Trái Tuyến
        df_vip_ko = build_vip_ko_dh_detail(
            df_visit_sched, mcp, report_date, filter_nv
        )
        st.markdown(render_vip_ko_dh_html(df_vip_ko), unsafe_allow_html=True)
        # Chi tiết ĐH line < 3 & Meat >= 4
        try:
          df_lt3 = build_orders_line_lt3_detail(df, report_date, filter_nv, mcp)
          st.markdown(render_orders_line_lt3_html(df_lt3), unsafe_allow_html=True)
        except Exception:
          pass
        try:
          df_meat4 = build_orders_meat_ge4_detail(df, report_date, filter_nv, mcp)
          st.markdown(render_orders_meat_ge4_html(df_meat4), unsafe_allow_html=True)
        except Exception:
          pass
        # ===== Metric ngày + Bảng tiến độ tháng (trước Chart) =====
        try:
          try:
            _moc = float(get_month_cfg().get('lppc_moc', 4.3) or 4.3)
          except Exception:
            _moc = 4.3
          # ASO ALL OFF/ON ngày:
          # TH = CH first-buy đúng ngày BC (logic ASO ALL)
          # CT = CH có lịch VT ngày đang chọn (theo kênh)
          # MTD = trong các CH thuộc lịch VT ngày đó, bao nhiêu CH đã có đơn từ đầu tháng → ngày BC
          _aso_off, _aso_on = {'th': 0, 'mtd': 0, 'ct': 0, 'ct_day': 0}, {'th': 0, 'mtd': 0, 'ct': 0, 'ct_day': 0}
          try:
            _rd0 = report_date if isinstance(report_date, date) else pd.Timestamp(report_date).date()
            _mstart = date(_rd0.year, _rd0.month, 1)

            def _thu_codes_for_date(d0):
              wd = d0.weekday()  # Mon=0
              code = str(wd + 2) if wd < 6 else 'CN'  # Mon=2 ... Sat=7
              cycles = {code}
              if code in ('2', '5'):
                cycles.add('25')
              if code in ('3', '6'):
                cycles.add('36')
              if code in ('4', '7'):
                cycles.add('47')
              return cycles

            _codes = _thu_codes_for_date(_rd0)

            def _nma(x):
              if pd.isna(x):
                return ''
              s = str(x).strip()
              if s.endswith('.0'):
                s = s[:-2]
              try:
                return str(int(float(s)))
              except Exception:
                return s

            # --- CT + tập CH lịch VT ngày (OFF/ON) từ MCP ---
            _route_off, _route_on = set(), set()
            if mcp is not None and not mcp.empty:
              c_ch = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH'])
              c_l1 = find_col(mcp, ['L1', 'Loại hình', 'Kênh'])
              c_nv = find_col(mcp, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
              c_thu = find_col(mcp, [
                  'Thứ', 'Thu', 'Visit day', 'Ngày VT', 'F', 'Frequency',
                  'Tần suất', 'Chu kỳ', 'Visit Day',
              ])
              _m = mcp
              if nv_selected(filter_nv) and c_nv:
                _m = filter_df_by_nv(mcp, c_nv, filter_nv)
              if c_ch and not _m.empty:
                if c_thu:
                  _thu = _m[c_thu].astype(str).str.strip()
                  _on_day = _thu.isin(_codes) | _thu.apply(
                      lambda x: any(c in str(x) for c in _codes if c != 'CN')
                  )
                  _mday = _m[_on_day]
                else:
                  _mday = _m
                if c_l1 and not _mday.empty:
                  _ml1 = _mday[c_l1].astype(str)
                  _route_off = set(
                      _mday.loc[_ml1.str.contains('Off', case=False, na=False), c_ch].map(_nma)
                  )
                  _route_on = set(
                      _mday.loc[_ml1.str.contains('On', case=False, na=False), c_ch].map(_nma)
                  )
                else:
                  _route_off = set(_mday[c_ch].map(_nma))
                _route_off.discard('')
                _route_on.discard('')

            # fallback CT từ Plan VT dòng TOTAL nếu MCP không ra
            if not _route_off or not _route_on:
              try:
                _tot = df_perf.iloc[-1]
                if not _route_off:
                  _aso_off['ct_day'] = int(round(float(_tot.get('Plan VT OFF', 0) or 0)))
                if not _route_on:
                  _aso_on['ct_day'] = int(round(float(_tot.get('Plan VT ON', 0) or 0)))
              except Exception:
                pass
            if _route_off:
              _aso_off['ct_day'] = len(_route_off)
            if _route_on:
              _aso_on['ct_day'] = len(_route_on)
            _aso_off['ct'] = _aso_off['ct_day']
            _aso_on['ct'] = _aso_on['ct_day']

            # --- TH + MTD từ RPT ---
            if df is not None and not df.empty and 'date' in df.columns and 'Mã CH' in df.columns:
              _mtd = df[(df['date'] >= _mstart) & (df['date'] <= _rd0)].copy()
              if nv_selected(filter_nv) and not _mtd.empty and 'Tên NVBH' in _mtd.columns:
                _mtd = filter_df_by_nv(_mtd, 'Tên NVBH', filter_nv)
              if not _mtd.empty:
                _mtd['_ma'] = _mtd['Mã CH'].map(_nma)
                _l1 = _mtd['L1'].astype(str) if 'L1' in _mtd.columns else pd.Series('', index=_mtd.index)
                for _key, _mask, _route in (
                    ('off', _l1.str.contains('Off', case=False, na=False), _route_off),
                    ('on', _l1.str.contains('On', case=False, na=False), _route_on),
                ):
                  _sub = _mtd[_mask]
                  if _sub.empty:
                    continue
                  # TH ngày: first-buy đúng ngày BC
                  _first = _sub.groupby('_ma')['date'].min()
                  _th = int((_first == _rd0).sum())
                  # MTD: CH thuộc lịch VT ngày đang chọn đã có đơn trong tháng
                  if _route:
                    _mtd_n = int(_sub[_sub['_ma'].isin(_route)]['_ma'].nunique())
                  else:
                    # fallback: toàn bộ CH kênh (hiếm khi MCP thiếu lịch)
                    _mtd_n = int(_sub['_ma'].nunique())
                  if _key == 'off':
                    _aso_off['th'] = _th
                    _aso_off['mtd'] = _mtd_n
                  else:
                    _aso_on['th'] = _th
                    _aso_on['mtd'] = _mtd_n
          except Exception:
            pass

          st.markdown(
              render_hs_daily_metric_cards(
                  df_perf, report_date, lppc_moc=_moc,
                  aso_off=_aso_off, aso_on=_aso_on,
              ),
              unsafe_allow_html=True,
          )
        except Exception as _e_daily:
          st.caption(f'(Metric ngày) {_e_daily}')
        try:
          _rd = report_date if isinstance(report_date, date) else pd.Timestamp(report_date).date()
          _wd, _el, _rem, _tg = get_timegone_stats(_rd)
          try:
            _tgts = get_targets()
          except Exception:
            _tgts = {}
          _rows = build_hs_monthly_kpi_rows(
              df, report_date, _tgts, turnover_targets, filter_nv, mcp
          )
          _co, _cn, _mc, _mb = build_hs_combo_mbs_summary(
              df, report_date,
              df_combo_off, df_combo_on, df_cat, df_brand,
              mcp, filter_nv,
          )
          st.markdown(
              render_hs_monthly_kpi_table(
                  _rows, _tg, combo_off=_co, combo_on=_cn,
                  mbs_cat=_mc, mbs_brand=_mb, report_date=_rd,
              ),
              unsafe_allow_html=True,
          )
        except Exception as _e_mon:
          st.caption(f'(Bảng tháng) {_e_mon}')

        # ===== Chart mức độ hoàn thành KPI theo ngày (từ dòng TOTAL 2 bảng) =====
        try:
          import plotly.graph_objects as go
          tot = df_perf.iloc[-1] if df_perf is not None and not df_perf.empty else None
          if tot is not None:
            # (label, %col, TH_col, CT_col) — text cột = TH/CT
            chart_items = [
                ('PC/VT OFF', '% PC/VT OFF', 'PC OFF', 'Đã VT OFF'),
                ('PC/Plan ON', '% PC/Plan ON', 'PC ON', 'Plan VT ON'),
                ('LPPC OFF', 'LPPC OFF', 'LPPC OFF', None),  # CT = mốc lương
                ('SellOut', '% TH SO', 'TH SO', 'CT Ngày SO'),
                ('ASO Xanh', '% TH Xanh', 'TH Xanh', 'CT Xanh'),
                ('ASO Vàng', '% TH Vàng', 'TH Vàng', 'CT Vàng'),
                ('Combo OFF', '% TH Combo OFF', 'TH Combo OFF', 'CT Combo OFF'),
                ('Combo ON', '% TH Combo ON', 'TH Combo ON', 'CT Combo ON'),
                ('TB', '% TH TB', 'Chụp hình bởi ĐDKD', 'Số CH TB PER'),
            ]

            def _num(x):
              try:
                s = str(x).replace('%', '').replace(',', '').replace('.', '').strip()
                # nếu là số dạng 1.234.567 hoặc 12.5
                s2 = str(x).replace('%', '').replace(',', '.').strip()
                if s2 and s2.lower() not in ('nan', 'none', ''):
                  return float(s2)
              except Exception:
                pass
              try:
                return float(x)
              except Exception:
                return 0.0

            labels, values, hover, is_lppc, text_thct = [], [], [], [], []
            for lab, col_pct, col_th, col_ct in chart_items:
              # % value
              raw_pct = tot.get(col_pct, 0) if col_pct else 0
              try:
                s = str(raw_pct).replace('%', '').replace(',', '.').strip()
                v = float(s) if s and s.lower() not in ('nan', 'none', '') else 0.0
              except Exception:
                v = 0.0

              th_v = _num(tot.get(col_th, 0)) if col_th else 0.0
              if col_ct is None and lab == 'LPPC OFF':
                try:
                  ct_v = float(get_month_cfg().get('lppc_moc', 4.3) or 4.3)
                except Exception:
                  ct_v = 4.3
                th_v = _num(tot.get('LPPC OFF', 0))
              else:
                ct_v = _num(tot.get(col_ct, 0)) if col_ct else 0.0

              # format TH/CT
              if lab == 'LPPC OFF':
                th_s = f'{th_v:.2f}'.rstrip('0').rstrip('.')
                ct_s = f'{ct_v:.1f}'.rstrip('0').rstrip('.')
              elif lab == 'SellOut':
                # số lớn → rút gọn
                def _fmt_n(n):
                  n = float(n or 0)
                  if abs(n) >= 1_000_000:
                    return f'{n/1_000_000:.1f}tr'
                  if abs(n) >= 1_000:
                    return f'{n/1_000:.0f}k'
                  return f'{int(round(n))}'
                th_s, ct_s = _fmt_n(th_v), _fmt_n(ct_v)
              else:
                th_s = str(int(round(th_v)))
                ct_s = str(int(round(ct_v)))

              labels.append(lab)
              values.append(v)
              is_lppc.append(lab == 'LPPC OFF')
              text_thct.append(f'{th_s}/{ct_s}')
              hover.append(f'{lab}: {th_s}/{ct_s} ({v}%)')

            if labels:
              try:
                _rd = report_date if isinstance(report_date, date) else pd.Timestamp(report_date).date()
                _, _, _, tg = get_timegone_stats(_rd)
                tg = float(tg or 0)
              except Exception:
                tg = 0.0
              # Palette tương phản — mỗi KPI 1 màu, không lặp
              _PALETTE = [
                  '#e53e3e', '#3182ce', '#38a169', '#dd6b20',
                  '#805ad5', '#d69e2e', '#319795', '#d53f8c',
                  '#2b6cb0', '#c05621', '#276749', '#6b46c1',
              ]
              colors = [_PALETTE[i % len(_PALETTE)] for i in range(len(values))]

              fig = go.Figure()
              text_labels = []
              for v, lp in zip(values, is_lppc):
                if lp:
                  text_labels.append(f'{v:.2f}')
                else:
                  text_labels.append(f'{v:.1f}%')
              fig.add_trace(go.Bar(
                  x=labels,
                  y=values,
                  text=text_labels,
                  textposition='outside',
                  marker_color=colors,
                  hovertext=hover,
                  hoverinfo='text',
              ))
              # Trục Y chính cho %; LPPC scale khác nên normalize display?
              # Giữ giá trị thật — LPPC ~4-6, % ~0-120 → LPPC sẽ thấp trên chart.
              # Scale LPPC lên % so với mốc để cùng trục % MTD
              y_plot = []
              text_labels2 = []
              hover2 = []
              for v, lp, lab, h, thct in zip(values, is_lppc, labels, hover, text_thct):
                if lp:
                  try:
                    moc = float(get_month_cfg().get('lppc_moc', 4.3) or 4.3)
                  except Exception:
                    moc = 4.3
                  # v đã là giá trị LPPC tuyệt đối trong values? 
                  # sau block mới: values vẫn là % (th/moc*100) nếu raw là LPPC số
                  # → scale lại nếu values là số LPPC thô
                  if v < 30:  # khả năng là giá trị LPPC thô
                    y_plot.append(round(v / moc * 100, 1) if moc else 0)
                  else:
                    y_plot.append(v)
                  text_labels2.append(f'{thct}')
                  hover2.append(h)
                else:
                  y_plot.append(v)
                  text_labels2.append(f'{thct}')
                  hover2.append(h)
              # % hoàn thành trên đỉnh mỗi cột
              pct_top = []
              for v, lp in zip(values, is_lppc):
                if lp:
                  try:
                    moc = float(get_month_cfg().get('lppc_moc', 4.3) or 4.3)
                  except Exception:
                    moc = 4.3
                  if v < 30:
                    pct_top.append(f'{round(v / moc * 100, 1) if moc else 0}%')
                  else:
                    pct_top.append(f'{float(v):.1f}%')
                else:
                  pct_top.append(f'{float(v):.1f}%')

              fig = go.Figure()
              # Cột chính: TH/CT bên trong
              fig.add_trace(go.Bar(
                  x=labels,
                  y=y_plot,
                  text=text_labels2,
                  textposition='inside',
                  textfont=dict(size=12, color='white', family='Arial Black'),
                  insidetextanchor='middle',
                  marker_color=colors,
                  hovertext=hover2,
                  hoverinfo='text',
                  name='TH/CT',
                  showlegend=False,
              ))
              # % trên đỉnh (trace trong suốt)
              fig.add_trace(go.Bar(
                  x=labels,
                  y=y_plot,
                  text=pct_top,
                  textposition='outside',
                  textfont=dict(size=12, color='#1a365d', family='Arial Black'),
                  marker_color='rgba(0,0,0,0)',
                  hoverinfo='skip',
                  name='% HT',
                  showlegend=False,
              ))
              if tg > 0:
                fig.add_hline(
                    y=tg, line_dash='dash', line_color='#3182ce', line_width=2,
                    annotation_text=f'Timegone {tg:.0f}%', annotation_position='top right',
                )
              fig.add_hline(
                  y=100, line_dash='dot', line_color='#718096', line_width=1,
                  annotation_text='100%', annotation_position='top left',
              )
              fig.update_layout(
                  title=dict(
                      text=f'Mức độ hoàn thành KPI theo ngày {report_date.strftime("%d/%m/%Y")}',
                      font=dict(size=15, color='#1a365d', family='Arial'),
                      x=0.5, xanchor='center',
                  ),
                  yaxis=dict(
                      title='% hoàn thành',
                      range=[0, max(130, (max(y_plot) + 25) if y_plot else 130)],
                      ticksuffix='%', gridcolor='#e2e8f0',
                  ),
                  barmode='overlay',
                  xaxis=dict(tickangle=-20, tickfont=dict(size=11)),
                  margin=dict(l=40, r=20, t=50, b=70),
                  height=380,
                  plot_bgcolor='white',
                  paper_bgcolor='white',
                  showlegend=False,
                  bargap=0.35,
              )
              st.plotly_chart(fig, use_container_width=True, config={
                  'displayModeBar': True,
                  'displaylogo': False,
                  'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
              })
        except Exception as _e_perf_chart:
          st.caption(f'Không vẽ được chart Hiệu Suất: {_e_perf_chart}')

        # Nhận xét nằm dưới các bảng chi tiết
        st.markdown(build_performance_comments(df_perf), unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
          st.download_button(
              '📥 Tải CSV Hiệu Suất',
              data=df_perf.to_csv(index=False).encode('utf-8-sig'),
              file_name=f'HieuSuat_{report_date}.csv',
              mime='text/csv',
              key='dl_perf',
          )
        with c2:
          if df_trai is not None and not df_trai.empty:
            st.download_button(
                '📥 Tải CSV ĐH Trái Tuyến',
                data=df_trai.to_csv(index=False).encode('utf-8-sig'),
                file_name=f'DH_TraiTuyen_{report_date}.csv',
                mime='text/csv',
                key='dl_trai',
            )
        with c3:
          if df_vip_ko is not None and not df_vip_ko.empty:
            st.download_button(
                '📥 Tải CSV VIP KO ĐH',
                data=df_vip_ko.to_csv(index=False).encode('utf-8-sig'),
                file_name=f'VIP_KO_DH_{report_date}.csv',
                mime='text/csv',
                key='dl_vip_ko',
            )

  elif selected_kpi == 'DISPLAY':
    st.markdown(
        '<h3 style="text-align:center;color:#1a365d;font-weight:800;">'
        '15. BÁO CÁO TRƯNG BÀY</h3>',
        unsafe_allow_html=True,
    )
    df_disp = load_display_data()
    if df_disp is None or df_disp.empty:
      st.warning(
          '⚠️ Chưa có file **DANH_SACH_KET_QUA_CUA_HANG_THAM_GIA_CHUONG_TRINH.xlsx** '
          'trong thư mục `data/`. Upload lên GitHub rồi **Xóa Cache & Reload**.'
      )
    else:
      df1, df2, df3, comments = build_display_report(df_disp, mcp, filter_nv)

      # ===== Options bộ lọc chung =====
      prog_names = []
      c_ct0 = find_col(df_disp, ['Tên chương trình', 'Chương trình', 'Tên CT'])
      if c_ct0:
        prog_names = sorted([
            str(p).strip() for p in df_disp[c_ct0].dropna().unique().tolist()
            if str(p).strip() and str(p).lower() != 'nan'
        ])
      if not prog_names and df2 is not None and not df2.empty:
        for c in df2.columns:
          if '|' in str(c):
            prog_names.append(str(c).split('|', 1)[0])
        seen = set()
        prog_names = [p for p in prog_names if not (p in seen or seen.add(p))]
      nv_names_tb = []
      if df1 is not None and not df1.empty and 'Tên NVBH' in df1.columns:
        nv_names_tb = sorted([
            str(x).strip() for x in df1['Tên NVBH'].dropna().unique().tolist()
            if str(x).strip() and str(x).lower() != 'nan'
            and 'tổng' not in str(x).lower() and 'total' not in str(x).lower()
        ])
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']

      # ===== Bộ lọc Bảng 1 (Tổng hợp) =====
      st.markdown(
          '<p class="filter-label" style="margin-top:8px;">🏷️ Bộ lọc Bảng tổng hợp</p>',
          unsafe_allow_html=True,
      )
      f1a, f1b, f1c = st.columns(3)
      with f1a:
        st.markdown(
            '<p class="filter-label">Chương Trình TB</p>',
            unsafe_allow_html=True,
        )
        f_prog_tb1 = st.multiselect(
            '',
            options=prog_names,
            default=[],
            key='disp_prog_tb1',
            label_visibility='collapsed',
            placeholder='Tất cả chương trình',
        )
      with f1b:
        st.markdown(
            '<p class="filter-label">Thứ VT</p>',
            unsafe_allow_html=True,
        )
        f_thu_tb1 = st.multiselect(
            '',
            options=thu_opts,
            default=[],
            key='disp_thu_tb1',
            label_visibility='collapsed',
            placeholder='Tất cả các thứ (2,3,4,5,6,7,25,36,47)',
        )
      with f1c:
        st.markdown(
            '<p class="filter-label">Tên NVBH</p>',
            unsafe_allow_html=True,
        )
        f_nv_tb1 = st.multiselect(
            '',
            options=nv_names_tb,
            default=[],
            key='disp_nv_tb1',
            label_visibility='collapsed',
            placeholder='Tất cả ĐDKD',
        )

      if f_prog_tb1 or f_thu_tb1 or f_nv_tb1:
        df1_view = rebuild_display_summary(
            df_disp, mcp,
            filter_nv=filter_nv,
            filter_thu=f_thu_tb1 or None,
            filter_nv_list=f_nv_tb1 or None,
            filter_prog=f_prog_tb1 or None,
        )
      else:
        df1_view = df1

      # Bảng 1
      st.markdown(render_display_summary_html(df1_view), unsafe_allow_html=True)

      # ===== Bộ lọc Bảng 2: Chương trình TB | Thứ VT | Tên NVBH =====
      st.markdown(
          '<p class="filter-label" style="margin-top:12px;">🏷️ Bộ lọc Bảng chi tiết theo CT</p>',
          unsafe_allow_html=True,
      )
      fc_p, fc_d, fc_n = st.columns(3)
      with fc_p:
        st.markdown(
            '<p class="filter-label">Chương Trình TB</p>',
            unsafe_allow_html=True,
        )
        f_prog_tb2 = st.multiselect(
            '',
            options=prog_names,
            default=[],
            key='disp_prog_tb2',
            label_visibility='collapsed',
            placeholder='Tất cả chương trình',
        )
      with fc_d:
        st.markdown(
            '<p class="filter-label">Thứ VT</p>',
            unsafe_allow_html=True,
        )
        f_thu_tb2 = st.multiselect(
            '',
            options=thu_opts,
            default=[],
            key='disp_thu_tb2',
            label_visibility='collapsed',
            placeholder='Tất cả các thứ (2,3,4,5,6,7,25,36,47)',
        )
      with fc_n:
        st.markdown(
            '<p class="filter-label">Tên NVBH</p>',
            unsafe_allow_html=True,
        )
        f_nv_tb2 = st.multiselect(
            '',
            options=nv_names_tb,
            default=[],
            key='disp_nv_tb2',
            label_visibility='collapsed',
            placeholder='Tất cả ĐDKD',
        )

      # Rebuild bảng 2 theo bộ lọc
      if f_thu_tb2 or f_nv_tb2 or f_prog_tb2:
        df2_view = rebuild_display_by_program(
            df_disp, mcp,
            filter_nv=filter_nv,
            filter_thu=f_thu_tb2 or None,
            filter_nv_list=f_nv_tb2 or None,
            filter_prog=f_prog_tb2 or None,
        )
      else:
        df2_view = df2

      # Bảng 2
      st.markdown(render_display_by_program_html(df2_view), unsafe_allow_html=True)

      # Bộ lọc bảng 3
      st.markdown(
          '<p class="filter-label" style="margin-top:14px;">🔍 Bộ lọc Chi Tiết KH</p>',
          unsafe_allow_html=True,
      )
      fc1, fc2, fc3, fc4, fc5, fc6 = st.columns(6)
      progs = sorted([
          p for p in df3['Tên Chương Trình TB'].dropna().unique().tolist()
          if str(p).strip() and str(p).lower() != 'nan'
      ]) if not df3.empty else []
      nvs = sorted([
          p for p in df3['Tên NVBH'].dropna().unique().tolist()
          if str(p).strip()
      ]) if not df3.empty else []
      thus = sorted([
          p for p in df3['Thứ VT'].dropna().unique().tolist()
          if str(p).strip() and str(p).lower() != 'nan'
      ]) if not df3.empty else []
      anh_opts = sorted([
          int(x) for x in df3['Số Bộ Ảnh Đã Chụp'].dropna().unique().tolist()
      ]) if (not df3.empty and 'Số Bộ Ảnh Đã Chụp' in df3.columns) else []
      with fc1:
        st.markdown('<p class="filter-label">Tên Chương Trình TB</p>', unsafe_allow_html=True)
        f_prog = st.multiselect('', progs, default=[], key='disp_prog', label_visibility='collapsed')
      with fc2:
        st.markdown('<p class="filter-label">Tên ĐDKD</p>', unsafe_allow_html=True)
        f_nv3 = st.multiselect('', nvs, default=[], key='disp_nv', label_visibility='collapsed')
      with fc3:
        st.markdown('<p class="filter-label">Mã KH</p>', unsafe_allow_html=True)
        f_ma3 = st.text_input('', key='disp_ma', label_visibility='collapsed', placeholder='Nhập Mã KH...')
      with fc4:
        st.markdown('<p class="filter-label">Tên KH</p>', unsafe_allow_html=True)
        f_ten3 = st.text_input('', key='disp_ten', label_visibility='collapsed', placeholder='Nhập Tên KH...')
      with fc5:
        st.markdown('<p class="filter-label">Thứ VT</p>', unsafe_allow_html=True)
        f_thu3 = st.multiselect('', thus, default=[], key='disp_thu', label_visibility='collapsed')
      with fc6:
        st.markdown('<p class="filter-label">Số Bộ Ảnh</p>', unsafe_allow_html=True)
        f_anh3 = st.multiselect(
            '', anh_opts, default=[], key='disp_anh',
            label_visibility='collapsed', placeholder='Tất cả',
        )

      df3f = df3.copy() if not df3.empty else df3
      if not df3f.empty:
        if f_prog:
          df3f = df3f[df3f['Tên Chương Trình TB'].isin(f_prog)]
        if f_nv3:
          df3f = df3f[df3f['Tên NVBH'].isin(f_nv3)]
        if f_ma3:
          df3f = df3f[df3f['Mã KH'].astype(str).str.contains(f_ma3.strip(), case=False, na=False)]
        if f_ten3:
          df3f = df3f[df3f['Tên KH'].astype(str).str.contains(f_ten3.strip(), case=False, na=False)]
        if f_thu3:
          df3f = df3f[df3f['Thứ VT'].astype(str).isin([str(x) for x in f_thu3])]
        if f_anh3:
          df3f = df3f[
              pd.to_numeric(df3f['Số Bộ Ảnh Đã Chụp'], errors='coerce')
              .fillna(0).astype(int)
              .isin([int(x) for x in f_anh3])
          ]

      st.markdown(render_display_detail_html(df3f), unsafe_allow_html=True)
      st.caption(f'Hiển thị: {len(df3f):,} / {len(df3):,} dòng')

      # Nhận xét
      st.markdown(comments, unsafe_allow_html=True)

      def _fmt_pct_cols(df_in):
        if df_in is None or df_in.empty:
          return df_in
        out = df_in.copy()
        for c in out.columns:
          cs = str(c)
          if cs.startswith('%') or '|%' in cs:
            def _one(x):
              if pd.isna(x) or str(x).strip() == '':
                return ''
              try:
                return f'{float(str(x).replace("%", "").strip()):.1f}%'
              except Exception:
                return x
            out[c] = out[c].map(_one)
        return out

      c1, c2, c3 = st.columns(3)
      with c1:
        if not df1.empty:
          st.download_button(
              '📥 Tải CSV Tổng Hợp TB',
              data=_fmt_pct_cols(df1).to_csv(index=False).encode('utf-8-sig'),
              file_name='TrungBay_TongHop.csv',
              mime='text/csv',
              key='dl_disp1',
          )
      with c2:
        if not df2.empty:
          st.download_button(
              '📥 Tải CSV Theo CT',
              data=_fmt_pct_cols(df2).to_csv(index=False).encode('utf-8-sig'),
              file_name='TrungBay_TheoCT.csv',
              mime='text/csv',
              key='dl_disp2',
          )
      with c3:
        if not df3f.empty:
          st.download_button(
              '📥 Tải CSV Chi Tiết KH',
              data=df3f.to_csv(index=False).encode('utf-8-sig'),
              file_name='TrungBay_ChiTietKH.csv',
              mime='text/csv',
              key='dl_disp3',
          )


  elif selected_kpi == 'PERF_CAT':
    st.markdown(
        '<h3 style="text-align:center;color:#1a365d;font-weight:800;">'
        '17. BÁO CÁO PERFORMANCE (THEO NGÀNH HÀNG)</h3>',
        unsafe_allow_html=True,
    )
    df_perf = load_perf_sku_data()
    if df_perf is None or df_perf.empty:
      st.warning(
          '⚠️ Chưa có file **TARGETACTUAL BY STD SKU -BY SM.xlsx** trong `data/`. '
          'Upload lên GitHub rồi **Xóa Cache & Reload**.'
      )
    else:
      data_by_m, months = build_perf_by_month(df_perf, filter_nv, n_months=4, df_rpt=df, report_date=report_date)
      if not months:
        st.info('Không có dữ liệu tháng để hiển thị.')
      else:
        st.caption(
            f'Nguồn: TARGETACTUAL BY STD SKU -BY SM | '
            f'Số liệu theo **triệu đồng** | SellOut **tháng T** lấy từ RPT (DanhSachChiTietDonHang); tháng trước lấy từ file Target/Actual | '
            f'{len(months)} tháng: {", ".join(months)}'
        )
        # ===== Bộ lọc bảng tổng hợp =====
        st.markdown(
            '<p class="filter-label">🔍 Bộ lọc bảng tổng hợp Performance</p>',
            unsafe_allow_html=True,
        )
        # Options
        c_month = find_col(df_perf, ['MONTH', 'Month'])
        c_nv_p = find_col(df_perf, ['SM NAME', 'SM_NAME', 'Tên NVBH'])
        c_cat_p = find_col(df_perf, ['SUB DIV', 'SUB_DIV', 'CAT'])
        all_months = months  # đã sort mới → cũ
        all_nvs = sorted(
            df_perf[c_nv_p].dropna().astype(str).str.strip().unique().tolist()
        ) if c_nv_p else []
        if filter_nv:
          all_nvs = [n for n in all_nvs if n in filter_nv] or all_nvs
        all_cats = sorted(
            df_perf[c_cat_p].dropna().astype(str).str.strip().unique().tolist()
        ) if c_cat_p else []
        all_cats = [c for c in all_cats if c and c.lower() not in ('nan', 'none', '', '(blank)')]

        f1, f2, f3 = st.columns(3)
        with f1:
          st.markdown('<p class="filter-label">Tháng</p>', unsafe_allow_html=True)
          f_months = st.multiselect(
              '', all_months, default=[all_months[0]] if all_months else [],
              key='perf_months', label_visibility='collapsed',
          )
        with f2:
          st.markdown('<p class="filter-label">Tên NVBH</p>', unsafe_allow_html=True)
          f_nvs = st.multiselect(
              '', all_nvs, default=[], key='perf_nvs', label_visibility='collapsed',
          )
        with f3:
          st.markdown('<p class="filter-label">SUB DIV</p>', unsafe_allow_html=True)
          f_cats = st.multiselect(
              '', all_cats, default=[], key='perf_cats', label_visibility='collapsed',
          )

        # Build matrix theo tháng đã chọn (gộp nếu nhiều tháng)
        use_months = f_months if f_months else ([all_months[0]] if all_months else [])
        use_nvs = f_nvs if f_nvs else (filter_nv if filter_nv else None)

        # Gộp nhiều tháng: cộng TARGET/SO
        mats = []
        cats_union = []
        for mm in use_months:
          dm, cm = build_perf_nv_matrix(df_perf, mm, use_nvs, df_rpt=df, report_date=report_date)
          if dm.empty:
            continue
          mats.append(dm)
          for c in cm:
            if c not in cats_union:
              cats_union.append(c)
        if f_cats:
          cats_union = [c for c in cats_union if c in f_cats]

        df_mat = pd.DataFrame()
        if mats:
          # Merge by Tên NVBH
          base = mats[0].copy()
          # drop total row for merge
          is_tot_mask = base['Tên NVBH'].astype(str).str.upper().str.contains('TỔNG')
          base_body = base[~is_tot_mask].copy()
          metric_cols = [
              c for c in base.columns
              if c not in ('STT', 'Tên NVBH') and (
                  c.endswith('|TARGET') or c.endswith('|SELL OUT') or c.endswith('|% MTD')
              )
          ]
          for extra in mats[1:]:
            eb = extra[~extra['Tên NVBH'].astype(str).str.upper().str.contains('TỔNG')].copy()
            keep_cols = ['Tên NVBH'] + [
                c for c in eb.columns
                if c not in ('STT', 'Tên NVBH') and (
                    c.endswith('|TARGET') or c.endswith('|SELL OUT')
                )
            ]
            eb = eb[[c for c in keep_cols if c in eb.columns]].copy()
            if eb.empty or 'Tên NVBH' not in base_body.columns:
              continue
            eb_idx = eb.drop_duplicates(subset=['Tên NVBH']).set_index('Tên NVBH')
            base_body = base_body.set_index('Tên NVBH')
            for c in eb_idx.columns:
              s_extra = pd.to_numeric(eb_idx[c], errors='coerce').fillna(0)
              if c in base_body.columns:
                base_body[c] = (
                    pd.to_numeric(base_body[c], errors='coerce').fillna(0).add(
                        s_extra, fill_value=0
                    )
                )
              else:
                base_body[c] = s_extra
                if c not in metric_cols:
                  metric_cols.append(c)
            only_extra = eb_idx.index.difference(base_body.index)
            if len(only_extra) > 0:
              base_body = pd.concat([base_body, eb_idx.loc[only_extra]], axis=0)
            base_body = base_body.reset_index()

          # Recompute % and TOTAL from cats_union
          for cat in cats_union:
            for suf in ('TARGET', 'SELL OUT', '% MTD'):
              col = f'{cat}|{suf}'
              if col not in base_body.columns:
                base_body[col] = 0.0
          # TOTAL
          base_body['TOTAL|TARGET'] = 0.0
          base_body['TOTAL|SELL OUT'] = 0.0
          for cat in cats_union:
            base_body['TOTAL|TARGET'] += pd.to_numeric(
                base_body.get(f'{cat}|TARGET', 0), errors='coerce'
            ).fillna(0)
            base_body['TOTAL|SELL OUT'] += pd.to_numeric(
                base_body.get(f'{cat}|SELL OUT', 0), errors='coerce'
            ).fillna(0)
            tg = pd.to_numeric(base_body[f'{cat}|TARGET'], errors='coerce').fillna(0)
            so = pd.to_numeric(base_body[f'{cat}|SELL OUT'], errors='coerce').fillna(0)
            base_body[f'{cat}|% MTD'] = [
                round(float(s) / float(t) * 100, 0) if float(t) > 0 else 0.0
                for t, s in zip(tg, so)
            ]
          base_body['TOTAL|% MTD'] = [
              round(float(s) / float(t) * 100, 0) if float(t) > 0 else 0.0
              for t, s in zip(base_body['TOTAL|TARGET'], base_body['TOTAL|SELL OUT'])
          ]
          base_body = base_body.sort_values('Tên NVBH').reset_index(drop=True)
          # Total row
          tot = {'Tên NVBH': 'TỔNG CỘNG', 'STT': ''}
          for cat in cats_union:
            tot[f'{cat}|TARGET'] = float(base_body[f'{cat}|TARGET'].sum())
            tot[f'{cat}|SELL OUT'] = float(base_body[f'{cat}|SELL OUT'].sum())
            t = tot[f'{cat}|TARGET']
            s = tot[f'{cat}|SELL OUT']
            tot[f'{cat}|% MTD'] = round(s / t * 100, 0) if t > 0 else 0.0
          tot['TOTAL|TARGET'] = float(base_body['TOTAL|TARGET'].sum())
          tot['TOTAL|SELL OUT'] = float(base_body['TOTAL|SELL OUT'].sum())
          tt, ts = tot['TOTAL|TARGET'], tot['TOTAL|SELL OUT']
          tot['TOTAL|% MTD'] = round(ts / tt * 100, 0) if tt > 0 else 0.0
          if 'STT' in base_body.columns:
            base_body = base_body.drop(columns=['STT'])
          base_body = base_body.reset_index(drop=True)
          base_body.insert(0, 'STT', range(1, len(base_body) + 1))
          df_mat = pd.concat([base_body, pd.DataFrame([tot])], ignore_index=True)

        label_m = ', '.join(use_months) if use_months else ''
        # Chỉ tô Timegone khi lọc đúng 1 tháng và đó là tháng T (mới nhất)
        _use_tg = (
            len(use_months) == 1
            and all_months
            and use_months[0] == all_months[0]
        )
        if not df_mat.empty and cats_union:
          st.markdown(
              render_perf_nv_matrix_html(
                  df_mat, cats_union, label_m, use_timegone=_use_tg
              ),
              unsafe_allow_html=True,
          )
          # 8 chart SUB DIV ngay dưới bảng tổng hợp (2×4)
          render_perf_subdiv_charts(df_mat, cats_union)
        elif use_months:
          st.info('Không có dữ liệu tổng hợp với bộ lọc hiện tại.')

        for _mi, m in enumerate(months):
          df_m = data_by_m.get(m)
          st.markdown(
              f'<h4 style="color:#1a365d;font-weight:800;margin:14px 0 6px 0;">'
              f'📅 Tháng {m}</h4>',
              unsafe_allow_html=True,
          )
          c_left, c_right = st.columns([1, 1.2])
          with c_left:
            # Tháng T (đầu list): Timegone; T-1..: mốc 100%
            html = render_perf_table_html(df_m, m, use_timegone=(_mi == 0))
            html = html.replace(
                f'<h4 style="color:#1a365d;font-weight:800;margin:12px 0 6px 0;">'
                f'📅 Tháng {m}</h4>',
                '',
            )
            st.markdown(html, unsafe_allow_html=True)
          with c_right:
            render_perf_chart(df_m, m)
          st.markdown(
              '<hr style="margin:14px 0;border:none;border-top:1px solid #e2e8f0;">',
              unsafe_allow_html=True,
          )

  elif selected_kpi == 'TEA_BATTLE':
    st.markdown(
        '<h3 style="text-align:center;color:#1a365d;font-weight:800;">'
        '16. KẾ HOẠCH TÁC CHIẾN TRÀ BÚP NON THÁNG 10</h3>',
        unsafe_allow_html=True,
    )
    df_raw = load_raw_tea_data()
    if df_raw is None or df_raw.empty:
      st.warning(
          '⚠️ Chưa có file **data.xlsx** (hoặc RAW DATA.xlsx) trong thư mục `data/`. '
          'Upload file data.xlsx / RAW Bev-Tea (3 tháng 7–9) lên GitHub rồi **Xóa Cache & Reload**.'
      )
    else:
      df_tea = build_tea_battle_report(df_raw, df, mcp, report_date, filter_nv)
      st.caption(
          'Nguồn: RAW DATA (RR) + RPT (MTD tháng BC) + MCP (VIP/Thứ VT) + file ĐK Tích Lũy (nếu có). | '
          'SỐ SUẤT: 10 thùng = 1 suất, max 2; dưới 10 thùng → 0 (RỚT).'
      )
      # Bảng tổng hợp NV (trên) — full data (đã theo filter_nv global nếu có)
      df_sum = build_tea_battle_summary(df_tea)
      st.markdown(render_tea_battle_summary_html(df_sum), unsafe_allow_html=True)

      # Bộ lọc nằm ngay trên bảng Chi tiết KH theo Nhân Viên
      st.markdown(
          '<p class="filter-label">🔍 Bộ lọc Chi tiết KH theo Nhân Viên (chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      nvs = sorted([
          x for x in df_tea['Tên NVBH'].dropna().unique().tolist() if str(x).strip()
      ]) if not df_tea.empty else []
      mas = sorted([
          str(x).replace('.0', '') for x in df_tea['Mã KH'].dropna().unique().tolist()
          if str(x).strip() and str(x).lower() != 'nan'
      ]) if not df_tea.empty and 'Mã KH' in df_tea.columns else []
      tens = sorted([
          str(x) for x in df_tea['Tên KH'].dropna().unique().tolist()
          if str(x).strip() and str(x).lower() != 'nan'
      ]) if not df_tea.empty and 'Tên KH' in df_tea.columns else []
      l1s = sorted([
          str(x) for x in df_tea['L1'].dropna().unique().tolist()
          if str(x).strip() and str(x).lower() != 'nan'
      ]) if not df_tea.empty else []
      thus = sorted([
          str(x) for x in df_tea['Thứ VT'].dropna().unique().tolist()
          if str(x).strip() and str(x).lower() != 'nan'
      ]) if not df_tea.empty else []
      mtd_tea_opts = []
      if not df_tea.empty and 'MTD TEA [Thùng]' in df_tea.columns:
        _vals = pd.to_numeric(df_tea['MTD TEA [Thùng]'], errors='coerce').dropna().unique().tolist()
        mtd_tea_opts = sorted(
            [str(v) if isinstance(v, str) else (str(int(v)) if float(v) == int(v) else str(v)) for v in _vals],
            key=lambda x: float(x) if x.replace('.', '', 1).isdigit() else 0,
        )
      elif not df_tea.empty:
        for c in df_tea.columns:
          if 'MTD' in str(c).upper() and 'TEA' in str(c).upper():
            _vals = pd.to_numeric(df_tea[c], errors='coerce').dropna().unique().tolist()
            mtd_tea_opts = sorted(
                [str(int(v)) if float(v) == int(v) else str(v) for v in _vals],
                key=lambda x: float(x) if x.replace('.', '', 1).isdigit() else 0,
            )
            break
      dk_opts = []
      if not df_tea.empty and 'ĐK D&L' in df_tea.columns:
        _dk = df_tea['ĐK D&L'].fillna('').astype(str).str.strip()
        _dk = _dk.replace({'': 'Chưa ĐK', 'nan': 'Chưa ĐK', 'None': 'Chưa ĐK'})
        _dk = _dk.apply(lambda x: '✓' if x in ('✓', '✔', '1', 'True', 'true') else (x if x else 'Chưa ĐK'))
        dk_opts = sorted(_dk.unique().tolist(), key=lambda x: (0 if x == '✓' else 1, x))

      r1c1, r1c2, r1c3, r1c4 = st.columns(4)
      with r1c1:
        st.markdown('<p class="filter-label">Tên NV</p>', unsafe_allow_html=True)
        f_nv_t = st.multiselect('', nvs, default=[], key='tea_nv', label_visibility='collapsed', placeholder='Tất cả NV')
      with r1c2:
        st.markdown('<p class="filter-label">Mã KH</p>', unsafe_allow_html=True)
        f_ma_t = st.multiselect('', mas, default=[], key='tea_ma', label_visibility='collapsed', placeholder='Tất cả Mã KH')
      with r1c3:
        st.markdown('<p class="filter-label">Tên KH</p>', unsafe_allow_html=True)
        f_ten_t = st.multiselect('', tens, default=[], key='tea_ten', label_visibility='collapsed', placeholder='Tất cả Tên KH')
      with r1c4:
        st.markdown('<p class="filter-label">L1</p>', unsafe_allow_html=True)
        f_l1_t = st.multiselect('', l1s, default=[], key='tea_l1', label_visibility='collapsed', placeholder='Tất cả L1')

      r2c1, r2c2, r2c3 = st.columns(3)
      with r2c1:
        st.markdown('<p class="filter-label">Thứ VT</p>', unsafe_allow_html=True)
        f_thu_t = st.multiselect('', thus, default=[], key='tea_thu', label_visibility='collapsed', placeholder='Tất cả Thứ VT')
      with r2c2:
        st.markdown('<p class="filter-label">MTD TEA</p>', unsafe_allow_html=True)
        f_mtd_tea = st.multiselect('', mtd_tea_opts, default=[], key='tea_mtd_tea', label_visibility='collapsed', placeholder='Tất cả MTD TEA')
      with r2c3:
        st.markdown('<p class="filter-label">ĐK D&L</p>', unsafe_allow_html=True)
        f_dk_t = st.multiselect('', dk_opts, default=[], key='tea_dk', label_visibility='collapsed', placeholder='Tất cả ĐK D&L')

      view = df_tea.copy()
      if not view.empty:
        if f_nv_t:
          view = view[view['Tên NVBH'].isin(f_nv_t)]
        if f_ma_t:
          view = view[view['Mã KH'].astype(str).str.replace(r'\.0$', '', regex=True).isin([str(x) for x in f_ma_t])]
        if f_ten_t:
          view = view[view['Tên KH'].astype(str).isin([str(x) for x in f_ten_t])]
        if f_l1_t:
          view = view[view['L1'].astype(str).isin([str(x) for x in f_l1_t])]
        if f_thu_t:
          view = view[view['Thứ VT'].astype(str).isin([str(x) for x in f_thu_t])]
        if f_mtd_tea:
          col_mtd = 'MTD TEA [Thùng]' if 'MTD TEA [Thùng]' in view.columns else None
          if col_mtd is None:
            for c in view.columns:
              if 'MTD' in str(c).upper() and 'TEA' in str(c).upper():
                col_mtd = c
                break
          if col_mtd:
            selected_nums = set()
            for x in f_mtd_tea:
              try:
                selected_nums.add(float(x))
              except Exception:
                pass
            _ser = pd.to_numeric(view[col_mtd], errors='coerce')
            view = view[_ser.isin(list(selected_nums))]
        if f_dk_t:
          _dk_col = view['ĐK D&L'].fillna('').astype(str).str.strip()
          _dk_norm = _dk_col.apply(
              lambda x: '✓' if x in ('✓', '✔', '1', 'True', 'true')
              else ('Chưa ĐK' if x in ('', 'nan', 'None') else x)
          )
          view = view[_dk_norm.isin([str(x) for x in f_dk_t])]
        view = view.drop(columns=['STT'], errors='ignore').reset_index(drop=True)
        view.insert(0, 'STT', range(1, len(view) + 1))

      # Bảng chi tiết KH theo Nhân Viên (dưới bộ lọc)
      st.markdown(render_tea_battle_html(view), unsafe_allow_html=True)
      st.caption(f'Hiển thị: {len(view):,} / {len(df_tea):,} cửa hàng')
      st.download_button(
          '📥 Tải CSV Kế hoạch Trà Búp Non',
          data=view.to_csv(index=False).encode('utf-8-sig'),
          file_name=f'TacChien_TraBupNon_{report_date}.csv',
          mime='text/csv',
          key='dl_tea_battle',
      )


  elif selected_kpi == 'WEEKLY_PREVIEW':
    st.markdown(
        '<h3 style="text-align:center;color:#1a365d;font-weight:800;">'
        'Weekly Review</h3>',
        unsafe_allow_html=True,
    )
    st.caption(
        'Map theo **Position code** | MCP = CH tạo ≤ ngày 4 tháng | '
        'ASO = bao phủ CH có đơn (giống ASO ALL) | %COV = ASO/MCP | Tách OFF / ON'
    )
    sales_hist = pd.DataFrame()
    df_off = pd.DataFrame()
    df_on = pd.DataFrame()
    try:
      sales_hist = load_weekly_sales()
      df_off, df_on = build_weekly_preview(
          mcp, sales_hist, df_rpt=df, filter_nv=filter_nv
      )
    except Exception as e:
      st.error('Lỗi chạy Weekly Preview: ' + str(e))
      st.exception(e)

    def _diag():
      data_files = []
      try:
        if os.path.isdir(get_data_dir()):
          data_files = sorted(os.listdir(get_data_dir()))
      except Exception:
        pass
      has_d2 = os.path.isfile(os.path.join(get_data_dir(), 'data-2.xlsx'))
      has_mcp = os.path.isfile(os.path.join(get_data_dir(), 'Data_MCP.xlsx'))
      n_sales = 0 if sales_hist is None else len(sales_hist)
      n_mcp = 0 if mcp is None else len(mcp)
      file_list = ', '.join(data_files) if data_files else '(trống)'
      st.info(
          'File trong data/: ' + file_list
          + ' | data-2.xlsx: ' + str(has_d2)
          + ' | Data_MCP.xlsx: ' + str(has_mcp)
          + ' | sales rows: ' + str(n_sales)
          + ' | mcp rows: ' + str(n_mcp)
      )

    # ---- Bảng OFF ----
    st.markdown(
        '<h4 style="color:#034ea2;font-weight:800;margin:12px 0 6px 0;">'
        'COV MCP OFF</h4>',
        unsafe_allow_html=True,
    )
    if df_off is None or df_off.empty:
      st.warning('Chưa có dữ liệu Weekly Preview — Kênh OFF.')
      _diag()
    else:
      st.markdown(render_weekly_preview_html(df_off, timegone_pct=_CURRENT_TIMEGONE), unsafe_allow_html=True)
      st.download_button(
          '📥 Tải CSV Weekly Preview OFF',
          data=df_off.to_csv(index=False).encode('utf-8-sig'),
          file_name=f'Weekly_Preview_OFF_{report_date.strftime("%Y%m%d")}.csv',
          mime='text/csv',
          key='dl_weekly_off',
      )

    # ---- Bảng ON ----
    st.markdown(
        '<h4 style="color:#034ea2;font-weight:800;margin:16px 0 6px 0;">'
        'COV MCP ON</h4>',
        unsafe_allow_html=True,
    )
    if df_on is None or df_on.empty:
      st.warning('Chưa có dữ liệu Weekly Preview — Kênh ON.')
    else:
      st.markdown(render_weekly_preview_html(df_on, timegone_pct=_CURRENT_TIMEGONE), unsafe_allow_html=True)
      st.download_button(
          '📥 Tải CSV Weekly Preview ON',
          data=df_on.to_csv(index=False).encode('utf-8-sig'),
          file_name=f'Weekly_Preview_ON_{report_date.strftime("%Y%m%d")}.csv',
          mime='text/csv',
          key='dl_weekly_on',
      )

    # ---- Bảng LPPC OFF ----
    st.markdown(
        '<h4 style="color:#034ea2;font-weight:800;margin:16px 0 6px 0;">'
        'LPPC OFF [ Not Meat/Beer ]</h4>',
        unsafe_allow_html=True,
    )
    try:
      df_lppc = build_weekly_lppc(
          mcp, sales_hist, df_rpt=df, filter_nv=filter_nv
      )
    except Exception as e:
      st.error('Lỗi LPPC Weekly: ' + str(e))
      st.exception(e)
      df_lppc = pd.DataFrame()
    if df_lppc is None or df_lppc.empty:
      st.warning('Chưa có dữ liệu LPPC Weekly — Kênh OFF.')
    else:
      st.markdown(
          render_weekly_lppc_html(df_lppc, timegone_pct=_CURRENT_TIMEGONE),
          unsafe_allow_html=True,
      )
      st.download_button(
          '📥 Tải CSV Weekly LPPC OFF',
          data=df_lppc.to_csv(index=False).encode('utf-8-sig'),
          file_name=f'Weekly_LPPC_OFF_{report_date.strftime("%Y%m%d")}.csv',
          mime='text/csv',
          key='dl_weekly_lppc',
      )

    # ---- Bảng LPPC OFF VIP3 / VIP5 / VIPSI ----
    st.markdown(
        '<h4 style="color:#034ea2;font-weight:800;margin:16px 0 6px 0;">'
        'LPPC OFF — Nhóm KH VIP (VIP3 + VIP5 + VIPSI) [ Not Meat/Beer ]</h4>',
        unsafe_allow_html=True,
    )
    try:
      df_lppc_vip = build_weekly_lppc_vip(
          mcp, sales_hist, df_rpt=df, filter_nv=filter_nv
      )
    except Exception as e:
      st.error('Lỗi LPPC VIP Weekly: ' + str(e))
      st.exception(e)
      df_lppc_vip = pd.DataFrame()
    if df_lppc_vip is None or df_lppc_vip.empty:
      st.warning('Chưa có dữ liệu LPPC VIP OFF (VIP3/VIP5/VIPSI).')
    else:
      st.markdown(
          render_weekly_lppc_vip_html(df_lppc_vip, timegone_pct=_CURRENT_TIMEGONE),
          unsafe_allow_html=True,
      )
      st.download_button(
          '📥 Tải CSV Weekly LPPC VIP OFF',
          data=df_lppc_vip.to_csv(index=False).encode('utf-8-sig'),
          file_name=f'Weekly_LPPC_VIP_OFF_{report_date.strftime("%Y%m%d")}.csv',
          mime='text/csv',
          key='dl_weekly_lppc_vip',
      )

    # ---- Bảng PC/SM/Day OFF ----
    st.markdown(
        '<h4 style="color:#034ea2;font-weight:800;margin:16px 0 6px 0;">'
        'PC/SM/DAY Kênh OFF</h4>',
        unsafe_allow_html=True,
    )
    try:
      df_pcday = build_weekly_pc_sm_day(
          mcp, sales_hist, df_rpt=df, filter_nv=filter_nv, report_date=report_date
      )
    except Exception as e:
      st.error('Lỗi PC/SM/Day Weekly: ' + str(e))
      st.exception(e)
      df_pcday = pd.DataFrame()
    if df_pcday is None or df_pcday.empty:
      st.warning('Chưa có dữ liệu PC/SM/Day — Kênh OFF.')
    else:
      st.markdown(render_weekly_pc_day_html(df_pcday), unsafe_allow_html=True)
      st.download_button(
          '📥 Tải CSV Weekly PC/SM/Day OFF',
          data=df_pcday.to_csv(index=False).encode('utf-8-sig'),
          file_name=f'Weekly_PC_SM_Day_OFF_{report_date.strftime("%Y%m%d")}.csv',
          mime='text/csv',
          key='dl_weekly_pcday',
      )

    # ---- Tổng hợp ĐH Trái Tuyến MTD ----
    st.markdown(
        '<h4 style="color:#034ea2;font-weight:800;margin:16px 0 6px 0;">'
        'ĐH Trái Tuyến MTD (đầu tháng → ngày BC)</h4>',
        unsafe_allow_html=True,
    )
    try:
      try:
        _vis = df_visit_sched
      except NameError:
        _vis = None
      if _vis is None or (hasattr(_vis, 'empty') and _vis.empty):
        try:
          _vis = load_visit_schedule()
        except Exception:
          _vis = pd.DataFrame()
      df_trai_mtd = build_weekly_trai_tuyen_mtd(
          df, _vis, mcp, report_date, filter_nv=filter_nv
      )
    except Exception as e:
      st.error('Lỗi tổng hợp ĐH Trái Tuyến MTD: ' + str(e))
      st.exception(e)
      df_trai_mtd = pd.DataFrame()
    if df_trai_mtd is None or df_trai_mtd.empty:
      st.warning('Chưa có dữ liệu ĐH Trái Tuyến MTD (cần file lịch VT + RPT).')
    else:
      st.markdown(render_weekly_trai_tuyen_html(df_trai_mtd), unsafe_allow_html=True)
      st.download_button(
          '📥 Tải CSV ĐH Trái Tuyến MTD',
          data=df_trai_mtd.to_csv(index=False).encode('utf-8-sig'),
          file_name=f'Weekly_TraiTuyen_MTD_{report_date.strftime("%Y%m%d")}.csv',
          mime='text/csv',
          key='dl_weekly_trai_mtd',
      )

    st.markdown(
        """
        <div class="note-box">
          <div style="font-weight:800;color:#034ea2;margin-bottom:6px;font-size:13px;">📌 LOGIC</div>
          <ul style="margin:0;padding-left:18px;line-height:1.55;font-size:12.5px;">
            <li><b>Đối chiếu theo Position code</b> (không theo tên NV) — ASO/MCP gắn với mã vị trí tuyến.</li>
            <li><b>MCP (tháng M):</b> Số CH trên MCP có Created_date ≤ ngày 4 tháng M, theo L1 OFF/ON.</li>
            <li><b>ASO (tháng M):</b> Số CH unique có đơn trong tháng M theo POS_CODE + L1 (giống ASO ALL).</li>
            <li><b>% COV:</b> ASO / MCP × 100. Tháng quá khứ mốc 100%; tháng hiện tại theo Timegone.</li>
            <li><b>ASO = 0 ở tháng cũ:</b> Position code đó chưa có giao dịch trong file data-2 (tuyến mới / đổi mã vị trí). Không phải lỗi map tên.</li>
            <li><b>LPPC Weekly (OFF):</b> Khác KPI lương. Chỉ L1 OFF, trừ Meat &amp; Beer, chỉ check line đạt MOQ. PC = mọi đơn có ≥1 line MOQ. LPPC = Tổng line MOQ / Tổng PC. Không lọc ≥4 line. Tháng 6–9 từ data-2; tháng 10 từ RPT.</li>
            <li><b>PC/SM/Day (OFF):</b> PC = max 1 PC/CH/ngày (CH có ≥1 line đạt MOQ) / số ngày làm việc trong tháng (trừ CN + lễ). Không trừ Meat/Beer, không lọc ≥4 line. Chỉ Kênh OFF.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


  elif selected_kpi != 'COMBO':
    set_color_moc_for_kpi(selected_kpi)
    df_r, team_tgt, title = build_report(

        df, report_date, targets, selected_kpi, filter_nv, mcp_df=mcp
    )
    if df_r is None or df_r.empty:
      st.warning(f'Không có dữ liệu báo cáo {selected_kpi}.')
      st.stop()
    total_row = df_r.iloc[-1]
    total_mtd = int(total_row['MTD'])
    total_ngay = int(total_row['Thực Hiện Ngày'])
    pct_col = '% MTD'
    pct_team = total_row[pct_col]
    st.markdown(
        f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px;'
        f' font-size: 16px; text-align: center;">{title} - THÁNG'
        f' {report_date.strftime("%m/%Y")}</h3>',
        unsafe_allow_html=True,
    )
    st.caption(
        f"⚡ Ngày: {report_date.strftime('%d/%m/%Y')} | Lọc: {nv_label(filter_nv)}"
    )
    st.markdown(
        f'<div style="text-align:center; font-size:12px; color:#7a1f1f; font-weight:700; margin:2px 0 8px;">💰 Mức lương KPI: {KPI_SALARY_LABEL.get(selected_kpi, "")}</div>',
        unsafe_allow_html=True,
    )
    if selected_kpi == 'ASO_ALL':
      _aso_off_only = get_month_cfg().get('aso_all_channel') == 'OFF'
      if _aso_off_only:
        c1, c2, c3, c4, c5 = st.columns(5)
      else:
        c1, c2, c3, c4, c5, c6 = st.columns(6)
      with c1:
        render_metric_card('🎯 Chỉ Tiêu MCP', f'{team_tgt:,}')
      with c2:
        render_metric_card('📈 MTD', f'{total_mtd:,}')
      with c3:
        render_metric_card('📊 % MTD', pct_team)
      with c4:
        render_metric_card('🆕 Ngày', f'+{total_ngay}')
      with c5:
        render_metric_card(
            'MCP OFF', f"{int(total_row.get('MTD OFF', 0)):,}/{int(total_row.get('MCP OFF', 0)):,}"
        )
      if not _aso_off_only:
        with c6:
          render_metric_card(
              'MCP ON', f"{int(total_row.get('MTD ON', 0)):,}/{int(total_row.get('MCP ON', 0)):,}"
          )
    else:
      c1, c2, c3, c4 = st.columns(4)
      with c1:
        render_metric_card('🎯 Target', f'{team_tgt:,}')
      with c2:
        render_metric_card('📈 MTD', f'{total_mtd:,}')
      with c3:
        render_metric_card('📊 % MTD', pct_team)
      with c4:
        render_metric_card('🆕 Ngày', f'+{total_ngay}')
    _df_show = df_r.copy()
    for _c in ['GAP']:
      if _c in _df_show.columns:
        _df_show[_c] = _df_show[_c].apply(
            lambda x: f'{int(round(float(x))):,}'.replace(',', '.')
            if isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.','').replace('-','').isdigit())
            else x
        )
    if 'Bình quân ngày' in _df_show.columns:
      _df_show['Bình quân ngày'] = _df_show['Bình quân ngày'].apply(
          lambda x: f'{float(x):,.1f}'.replace(',', '.')
          if isinstance(x, (int, float))
          else x
      )
    st.markdown(render_html_table(_df_show), unsafe_allow_html=True)
    df_eval = df_r.iloc[:-1].copy()
    _pc = '% MTD'
    df_eval['_pct_val'] = (
        df_eval[_pc].astype(str).str.replace('%', '').astype(float)
    )

    df_sorted_pct = df_eval.sort_values(by='_pct_val', ascending=False)
    top3 = df_sorted_pct.head(3)
    bottom3 = df_sorted_pct.tail(3).iloc[::-1]

    top3_text = ', '.join(
        [f"{r['Tên NVBH']} ({r[_pc]})" for _, r in top3.iterrows()]
    )
    bottom3_text = ', '.join(
        [f"{r['Tên NVBH']} ({r[_pc]})" for _, r in bottom3.iterrows()]
    )
    st.markdown(
        f"""
        <div class="note-box">
            <div style="font-weight: 800; color: #034ea2; margin-bottom: 8px; font-size: 13.5px;">NHẬN XÉT & ĐÁNH GIÁ CHỈ SỐ {title.upper()}:</div>
            <ul style="margin: 0; padding-left: 18px; line-height: 1.6;">
                <li><b>Kết Quả Thực Hiện:</b> Đạt {total_mtd:,} / {team_tgt:,} ({pct_team} MTD). Phát sinh ngày: +{total_ngay}.</li>
                <li><b>Top 3 ĐDKD Dẫn Đầu:</b> {top3_text}.</li>
                <li><b>Bottom 3 ĐDKD Cần Cải Thiện:</b> {bottom3_text}.</li>
                <li><b>Đề Xuất Hành Động Cho 3 Bạn Bottom:</b> Tập trung rà soát tuyến chưa mua, đẩy mạnh combo kích cầu và SS đồng hành đi thị trường (Field Coaching) trong 2 ngày tới.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

  else:
    df_combo, target_off_total, target_on_total = build_combo_matrix(
        df, report_date, df_combo_off, df_combo_on, filter_nv, mcp_df=mcp
    )
    total_row = df_combo.iloc[-1]
    # Mốc tô màu Combo = % MTD dòng Total (trung bình OFF/ON nếu có)
    try:
      _p_off = float(str(total_row.get('% MTD (OFF)', '0')).replace('%', ''))
      _p_on = float(str(total_row.get('% MTD (ON)', '0')).replace('%', ''))
      _combo_moc = round((_p_off + _p_on) / 2, 1) if (_p_off or _p_on) else 100.0
    except Exception:
      _combo_moc = 100.0
    set_color_moc_for_kpi('COMBO', total_pct=_combo_moc)
    total_off = int(total_row['MTD (OFF)'])
    total_on = int(total_row['MTD (ON)'])
    ngay_off = int(total_row['Phát sinh Ngày (OFF)'])
    ngay_on = int(total_row['Phát sinh Ngày (ON)'])

    pct_off_team = (
        round(total_off / target_off_total * 100, 1)
        if target_off_total
        else 0
    )
    pct_on_team = (
        round(total_on / target_on_total * 100, 1) if target_on_total else 0
    )

    st.markdown(
        f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px;'
        f' font-size: 16px; text-align: center;">BÁO CÁO ĐH COMBO (MATRIX OFF/ON) - THÁNG'
        f' {report_date.strftime("%m/%Y")}</h3>',
        unsafe_allow_html=True,
    )
    st.caption(
        f"⚡ Ngày: {report_date.strftime('%d/%m/%Y')} | Lọc: {filter_nv} | Target"
        f' OFF: {target_off_total} CH | Target ON: {target_on_total} CH'
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
      render_metric_card(
          'MTD OFF / Target',
          f'{total_off:,} / {target_off_total:,} ({pct_off_team}%)',
      )
    with c2:
      render_metric_card(
          'MTD ON / Target',
          f'{total_on:,} / {target_on_total:,} ({pct_on_team}%)',
      )
    with c3:
      render_metric_card('Phát sinh Ngày (OFF)', f'+{ngay_off}')
    with c4:
      render_metric_card('Phát sinh Ngày (ON)', f'+{ngay_on}')

    df_eval_off = df_combo.iloc[:-1].copy()
    df_eval_off['_pct_val_off'] = (
        df_eval_off['% MTD (OFF)'].str.replace('%', '').astype(float)
    )
    df_sorted_off = df_eval_off.sort_values(
        by='_pct_val_off', ascending=False
    )
    top3_off = df_sorted_off.head(3)
    bottom3_off = df_sorted_off.tail(3).iloc[::-1]

    top3_off_text = ', '.join(
        [f"{r['Tên NVBH']} ({r['% MTD (OFF)']})" for _, r in top3_off.iterrows()]
    )
    bottom3_off_text = ', '.join(
        [
            f"{r['Tên NVBH']} ({r['% MTD (OFF)']})"
            for _, r in bottom3_off.iterrows()
        ]
    )

    st.markdown(render_html_table(df_combo), unsafe_allow_html=True)

    # Chi tiết đơn hàng Combo phát sinh đúng ngày đang chọn, format giống Báo Cáo Hiệu Suất.
    df_combo_orders = build_combo_orders_detail(
        df, report_date, filter_nv, mcp_df=mcp
    )
    st.markdown(render_combo_orders_html(df_combo_orders), unsafe_allow_html=True)

    # KH DS Combo có ĐH ≥ ngưỡng DS nhưng không có KM Combo
    df_miss_off = build_combo_miss_detail(
        df, report_date, df_combo_off, 'OFF', filter_nv, mcp_df=mcp
    )
    df_miss_on = build_combo_miss_detail(
        df, report_date, df_combo_on, 'ON', filter_nv, mcp_df=mcp
    )

    # ---- Bộ lọc chung cho 3 bảng miss ----
    _miss_all = pd.concat(
        [x for x in [df_miss_off, df_miss_on] if x is not None and not x.empty],
        ignore_index=True,
    ) if (
        (df_miss_off is not None and not df_miss_off.empty)
        or (df_miss_on is not None and not df_miss_on.empty)
    ) else pd.DataFrame()

    def _opts(col):
      if _miss_all.empty or col not in _miss_all.columns:
        return []
      return sorted([
          str(x) for x in _miss_all[col].dropna().astype(str).str.strip().unique()
          if str(x).strip() and str(x).strip().lower() not in ('nan', 'none', '')
      ])

    st.markdown(
        '<p style="font-weight:800;color:#034ea2;margin:12px 0 4px 0;font-size:13px;">'
        '🔎 Bộ lọc bảng Miss Combo (áp dụng chung 3 bảng)</p>',
        unsafe_allow_html=True,
    )
    f1, f2, f3 = st.columns(3)
    with f1:
      st.markdown('<p class="filter-label">👤 Tên NVBH</p>', unsafe_allow_html=True)
      miss_f_nv = st.multiselect(
          'miss_nv', _opts('Tên NVBH'), default=[],
          key='combo_miss_nv', label_visibility='collapsed',
      )
    with f2:
      st.markdown('<p class="filter-label">🆔 Mã KH</p>', unsafe_allow_html=True)
      miss_f_ma = st.multiselect(
          'miss_ma', _opts('Mã KH'), default=[],
          key='combo_miss_ma', label_visibility='collapsed',
      )
    with f3:
      st.markdown('<p class="filter-label">🏪 Tên KH</p>', unsafe_allow_html=True)
      miss_f_ten = st.multiselect(
          'miss_ten', _opts('Tên KH'), default=[],
          key='combo_miss_ten', label_visibility='collapsed',
      )
    f4, f5, f6 = st.columns(3)
    with f4:
      st.markdown('<p class="filter-label">📅 Ngày ĐH (lịch tháng)</p>', unsafe_allow_html=True)
      _rd = report_date.date() if hasattr(report_date, 'date') else report_date
      _ms = date(_rd.year, _rd.month, 1)
      try:
        miss_f_ngay = st.date_input(
            'miss_ngay',
            value=(_ms, _rd),
            min_value=_ms,
            max_value=_rd,
            format='DD/MM/YYYY',
            key='combo_miss_ngay',
            label_visibility='collapsed',
        )
      except Exception:
        miss_f_ngay = st.date_input(
            'miss_ngay',
            value=_rd,
            min_value=_ms,
            max_value=_rd,
            format='DD/MM/YYYY',
            key='combo_miss_ngay',
            label_visibility='collapsed',
        )
    with f5:
      st.markdown('<p class="filter-label">🏷️ L1</p>', unsafe_allow_html=True)
      miss_f_l1 = st.multiselect(
          'miss_l1', _opts('Loại Hình L1'), default=[],
          key='combo_miss_l1', label_visibility='collapsed',
      )
    with f6:
      st.write('')

    def _apply_miss_filters(df_in):
      if df_in is None or df_in.empty:
        return df_in if df_in is not None else pd.DataFrame()
      out = df_in.copy()
      if miss_f_nv and 'Tên NVBH' in out.columns:
        out = out[out['Tên NVBH'].astype(str).str.strip().isin(miss_f_nv)]
      if miss_f_ma and 'Mã KH' in out.columns:
        out = out[out['Mã KH'].astype(str).str.strip().isin(miss_f_ma)]
      if miss_f_ten and 'Tên KH' in out.columns:
        out = out[out['Tên KH'].astype(str).str.strip().isin(miss_f_ten)]
      # Ngày ĐH: lịch tháng (range hoặc 1 ngày)
      if miss_f_ngay is not None and 'Ngày ĐH' in out.columns:
        try:
          if isinstance(miss_f_ngay, (list, tuple)) and len(miss_f_ngay) == 2:
            d0, d1 = miss_f_ngay[0], miss_f_ngay[1]
            if d0 is not None and d1 is not None:
              def _in_range(s):
                try:
                  dt = pd.to_datetime(str(s), dayfirst=True, errors='coerce')
                  if pd.isna(dt):
                    return False
                  dd = dt.date() if hasattr(dt, 'date') else dt
                  return d0 <= dd <= d1
                except Exception:
                  return False
              out = out[out['Ngày ĐH'].apply(_in_range)]
          elif hasattr(miss_f_ngay, 'strftime'):
            # single date
            ds = miss_f_ngay.strftime('%d/%m/%Y')
            out = out[out['Ngày ĐH'].astype(str).str.strip() == ds]
        except Exception:
          pass
      if miss_f_l1 and 'Loại Hình L1' in out.columns:
        out = out[out['Loại Hình L1'].astype(str).str.strip().isin(miss_f_l1)]
      if not out.empty and 'STT' in out.columns:
        out = out.reset_index(drop=True)
        # giữ dòng TỔNG nếu có
        is_tot = out['Tên NVBH'].astype(str).str.upper().str.contains('TỔNG|TOTAL', na=False)
        body = out[~is_tot].copy()
        if not body.empty and 'STT' in body.columns:
          body['STT'] = range(1, len(body) + 1)
        tot = out[is_tot]
        out = pd.concat([body, tot], ignore_index=True) if not tot.empty else body
      return out

    df_miss_off_f = _apply_miss_filters(df_miss_off)
    df_miss_on_f = _apply_miss_filters(df_miss_on)
    df_miss_sum = build_combo_miss_summary(df_miss_off_f, df_miss_on_f)

    if df_miss_sum is not None and not df_miss_sum.empty:
      st.markdown(
          '<p style="font-weight:800;color:#034ea2;margin:14px 0 6px 0;">'
          '📊 TỔNG HỢP THEO NHÂN VIÊN — ĐH đạt ngưỡng DS nhưng chưa có KM Combo'
          ' <span style="font-weight:600;font-size:12px;color:#718096;">'
          '(OFF ≥ 800.000đ · ON ≥ 300.000đ)</span></p>',
          unsafe_allow_html=True,
      )
      st.markdown(render_html_table(df_miss_sum), unsafe_allow_html=True)
    else:
      st.caption('Không có dữ liệu tổng hợp miss Combo với bộ lọc hiện tại.')

    _n_off = 0 if df_combo_off is None or df_combo_off.empty else len(df_combo_off)
    _n_on = 0 if df_combo_on is None or df_combo_on.empty else len(df_combo_on)
    if df_miss_off_f is not None and not df_miss_off_f.empty:
      render_combo_miss_table(
          df_miss_off_f, 'CHI TIẾT ĐH COMBO OFF', 'combo_miss_off'
      )
      st.caption(
          f'Đối chiếu DS Combo OFF ({_n_off:,} CH) · {len(df_miss_off_f):,} đơn hàng'
      )
    else:
      st.markdown(
          '<p style="font-weight:800;color:#1a365d;margin:8px 0 4px 0;">'
          '📋 CHI TIẾT ĐH COMBO OFF</p>',
          unsafe_allow_html=True,
      )
      st.caption('Không có KH trong DS Combo OFF đạt ĐK chính mà thiếu KM Combo (theo bộ lọc).')

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    if df_miss_on_f is not None and not df_miss_on_f.empty:
      render_combo_miss_table(
          df_miss_on_f, 'CHI TIẾT ĐH COMBO ON', 'combo_miss_on'
      )
      st.caption(
          f'Đối chiếu DS Combo ON ({_n_on:,} CH) · {len(df_miss_on_f):,} đơn hàng'
      )
    else:
      st.markdown(
          '<p style="font-weight:800;color:#1a365d;margin:8px 0 4px 0;">'
          '📋 CHI TIẾT ĐH COMBO ON</p>',
          unsafe_allow_html=True,
      )
      st.caption('Không có KH trong DS Combo ON đạt ĐK chính mà thiếu KM Combo (theo bộ lọc).')


    st.markdown(
        f"""
        <div class="note-box">
            <div style="font-weight: 800; color: #034ea2; margin-bottom: 8px; font-size: 13.5px;">NHẬN XÉT & ĐÁNH GIÁ BÁO CÁO ĐH COMBO (MATRIX OFF/ON):</div>
            <ul style="margin: 0; padding-left: 18px; line-height: 1.6;">
                <li><b>Kết Quả Thực Hiện:</b> Kênh OFF đạt <b>{total_off:,} / {target_off_total:,} CH ({pct_off_team}%)</b> (Phát sinh ngày: +{ngay_off} CH) | Kênh ON đạt <b>{total_on:,} / {target_on_total:,} CH ({pct_on_team}%)</b> (Phát sinh ngày: +{ngay_on} CH).</li>
                <li><b>Top 3 ĐDKD Dẫn Đầu (OFF):</b> {top3_off_text}.</li>
                <li><b>Bottom 3 ĐDKD Cần Cải Thiện (OFF):</b> {bottom3_off_text}.</li>
                <li><b>Đề Xuất Hành Động Cho 3 Bạn Bottom:</b> Tập trung rà soát các cửa hàng trong danh sách combo chưa phát sinh đơn hàng, kiểm tra trưng bày sản phẩm và kích hoạt chương trình khuyến mại đẩy mạnh doanh số.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Các hàm cập nhật query params cho các tab khác
def update_mcp_params():
  st.query_params['mcp_nv'] = (
      ','.join(st.session_state.mcp_nv_input)
      if st.session_state.mcp_nv_input
      else ''
  )
  st.query_params['mcp_thu'] = (
      ','.join(st.session_state.mcp_thu_input)
      if st.session_state.mcp_thu_input
      else ''
  )
  st.query_params['mcp_ma'] = st.session_state.mcp_ma_input
  st.query_params['mcp_ten'] = st.session_state.mcp_ten_input
  st.query_params['mcp_vip'] = (
      ','.join(st.session_state.mcp_vip_input)
      if st.session_state.mcp_vip_input
      else ''
  )
  st.query_params['mcp_l1'] = (
      ','.join(st.session_state.mcp_l1_input)
      if st.session_state.get('mcp_l1_input')
      else ''
  )
  st.query_params['mcp_ds'] = (
      ','.join(st.session_state.mcp_ds_input)
      if st.session_state.mcp_ds_input
      else ''
  )


def update_cat_params():
  st.query_params['cat_nv'] = (
      ','.join(st.session_state.cat_nv_input)
      if st.session_state.cat_nv_input
      else ''
  )
  st.query_params['cat_thu'] = (
      ','.join(st.session_state.cat_thu_input)
      if st.session_state.cat_thu_input
      else ''
  )
  st.query_params['cat_ma'] = st.session_state.cat_ma_input
  st.query_params['cat_ten'] = st.session_state.cat_ten_input


def update_brand_params():
  st.query_params['brand_nv'] = (
      ','.join(st.session_state.brand_nv_input)
      if st.session_state.brand_nv_input
      else ''
  )
  st.query_params['brand_thu'] = (
      ','.join(st.session_state.brand_thu_input)
      if st.session_state.brand_thu_input
      else ''
  )
  st.query_params['brand_ma'] = st.session_state.brand_ma_input
  st.query_params['brand_ten'] = st.session_state.brand_ten_input


def update_off_params():
  st.query_params['off_nv'] = (
      ','.join(st.session_state.off_nv_input)
      if st.session_state.off_nv_input
      else ''
  )
  st.query_params['off_thu'] = (
      ','.join(st.session_state.off_thu_input)
      if st.session_state.off_thu_input
      else ''
  )
  st.query_params['off_ma'] = st.session_state.off_ma_input
  st.query_params['off_ten'] = st.session_state.off_ten_input


def update_on_params():
  st.query_params['on_nv'] = (
      ','.join(st.session_state.on_nv_input)
      if st.session_state.on_nv_input
      else ''
  )
  st.query_params['on_thu'] = (
      ','.join(st.session_state.on_thu_input)
      if st.session_state.on_thu_input
      else ''
  )
  st.query_params['on_ma'] = st.session_state.on_ma_input
  st.query_params['on_ten'] = st.session_state.on_ten_input


# ====================== MBS CAT/BRAND SUMMARY ======================
def build_mbs_data_summary(df_source, kind='CAT'):
  """Tạo bảng Summary MBS CAT/BRAND từ Data_MBS đã được tính doanh số từ RPT_061.

  - Doanh số: dùng các cột Doanh số thực đạt đã được process từ RPT_061.
  - Số lượng ngành/nhãn hàng: count từng dòng trong Data_Cat/Data_Brand.
  - OLD = Cũ, NEW = Mới, FOCUS = Duy trì.
  - OLD đã mua = dòng OLD có doanh số thực đạt > 0.
  - FOCUS cần duy trì = count tất cả dòng FOCUS (không cần DS).
  - FOCUS đã mua (đã duy trì) = FOCUS có DS >= 200.000.
  - NEW đã mở thêm = NEW có DS >= 200.000.
  - Mới duy trì/mở thành công = FOCUS đạt >= 200k + NEW đạt >= 200k.
  """
  if df_source is None or df_source.empty:
    return pd.DataFrame()

  df_s = df_source.copy()
  kind_u = str(kind).upper().strip()
  if kind_u == 'BRAND':
    col_uid = find_col(df_s, ['SM UID'])
    col_nv = find_col(df_s, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    col_code = find_col(df_s, ['Outlet Code', 'Outlet_code', 'Mã CH', 'Mã khách hàng'])
    col_name = find_col(df_s, ['Outlet Name', 'Outlet_name', 'Tên CH', 'Tên khách hàng'])
    col_target = find_col(df_s, ['Doanh số nền tảng của OUTLET', 'Doanh so nen tang', 'Target', 'Chỉ tiêu'])
    col_actual = find_col(df_s, ['Doanh số thực đạt của brand', 'Doanh số thực đạt BRAND'])
    col_actual_nc = find_col(df_s, [
        'Doanh số thực đạt của brand (Not Cancel/Pending)',
        'Doanh số thực đạt của brand(Not Cancel/Pending)',
    ])
    col_type = find_col(df_s, ['Phân loại brand', 'Phan loai brand', 'Loại brand'])
    col_bonus = find_col(df_s, ['Điểm thưởng dự kiến'])
  else:
    col_uid = find_col(df_s, ['SM UID'])
    col_nv = find_col(df_s, ['Tên NVBH', 'SM Name', 'SM name', 'Nhân viên'])
    col_code = find_col(df_s, ['Outlet Code', 'Outlet_code', 'Mã CH', 'Mã khách hàng'])
    col_name = find_col(df_s, ['Outlet Name', 'Outlet_name', 'Tên CH', 'Tên khách hàng'])
    col_target = find_col(df_s, ['Doanh số nền tảng của OUTLET', 'Doanh so nen tang', 'Target', 'Chỉ tiêu'])
    col_actual = find_col(df_s, ['Doanh số thực đạt của CAT', 'Doanh số thực đạt CAT'])
    col_actual_nc = find_col(df_s, [
        'Doanh số thực đạt của CAT(Not Cancel/Pending)',
        'Doanh số thực đạt của CAT (Not Cancel/Pending)',
    ])
    col_type = find_col(df_s, ['Phân loại cat', 'Phan loai cat', 'Loại cat'])
    col_bonus = find_col(df_s, ['Điểm thưởng dự kiến của OUTLET', 'Điểm thưởng dự kiến'])

  if not col_code:
    return pd.DataFrame()

  df_s['_summary_code'] = df_s[col_code].astype(str).str.strip()
  df_s['_summary_actual'] = (
      pd.to_numeric(df_s[col_actual], errors='coerce').fillna(0.0)
      if col_actual else 0.0
  )
  df_s['_summary_actual_nc'] = (
      pd.to_numeric(df_s[col_actual_nc], errors='coerce').fillna(0.0)
      if col_actual_nc else df_s['_summary_actual']
  )
  df_s['_summary_target'] = (
      pd.to_numeric(df_s[col_target], errors='coerce').fillna(0.0)
      if col_target else 0.0
  )
  df_s['_summary_type'] = (
      df_s[col_type].astype(str).str.strip().str.upper()
      if col_type else ''
  )
  df_s['_summary_bought'] = df_s['_summary_actual'] > 0

  rows = []
  for code, sub in df_s.groupby('_summary_code', sort=False):
    if not str(code).strip() or str(code).lower() in ('nan', 'none'):
      continue

    first = sub.iloc[0]
    old_mask = sub['_summary_type'].eq('OLD')
    new_mask = sub['_summary_type'].eq('NEW')
    focus_mask = sub['_summary_type'].eq('FOCUS')

    # OLD: cần mua = tất cả OLD; đã mua = OLD có DS > 0
    # FOCUS: cần duy trì = tất cả FOCUS; đã mua = FOCUS có DS >= 200.000
    # NEW: đã mở thêm = NEW có DS >= 200.000
    mbs_200k = sub['_summary_actual'] >= 200000
    new_qualified = new_mask & mbs_200k
    focus_qualified = focus_mask & mbs_200k

    old_need = int(old_mask.sum())
    old_bought = int((old_mask & sub['_summary_bought']).sum())
    focus_need = int(focus_mask.sum())          # tất cả FOCUS cần duy trì
    focus_bought = int(focus_qualified.sum())   # FOCUS đã đạt >= 200k
    new_opened = int(new_qualified.sum())
    successful_new = focus_bought + new_opened
    total_bought = old_bought + focus_bought + new_opened

    target = float(sub['_summary_target'].iloc[0] or 0)
    actual = float(sub['_summary_actual'].sum() or 0)
    actual_nc = float(sub['_summary_actual_nc'].sum() or 0)
    pct = round(actual / target * 100, 1) if target else 0.0

    rows.append({
        'SM UID': first[col_uid] if col_uid else '',
        'SM Name': first[col_nv] if col_nv else '',
        'Outlet Code': code,
        'Outlet Name': first[col_name] if col_name else '',
        'Chỉ tiêu doanh số': target,
        'Doanh số thực hiện (Paid & Invoiced)': actual,
        'Doanh số thực hiện ( Not Cancel/Pending)': actual_nc,
        '% Th/CT (Paid & Invoiced)': pct,
        'SL ngành/nhãn hàng cũ cần mua/đã mua': f'{old_need}/{old_bought}',
        'SL ngành/nhãn hàng mới cần duy trì/đã mua': f'{focus_need}/{focus_bought}',
        'SL ngành/nhãn hàng mới đã mở thêm': new_opened,
        'Tổng SL ngành/nhãn hàng mới duy trì/mở thành công': successful_new,
        'Tổng SL ngành/nhãn hàng đã mua': total_bought,
        'Điểm thưởng dự kiến': (
            float(pd.to_numeric(sub[col_bonus], errors='coerce').dropna().iloc[0])
            if col_bonus and not pd.to_numeric(sub[col_bonus], errors='coerce').dropna().empty
            else 0.0
        ),
    })

  out = pd.DataFrame(rows)
  if out.empty:
    return out
  return out.sort_values(['SM Name', 'Outlet Code'], kind='stable').reset_index(drop=True)


def render_mbs_data_table(df_show, selected_cols):
  """Bảng Data MBS CAT/BRAND: luôn sticky STT | Tên nhóm | Outlet Code | Tên CH."""
  if df_show is None or df_show.empty or not selected_cols:
    return

  def _freeze_key(col):
    cl = str(col).lower().strip()
    cl_nospace = cl.replace(' ', '').replace('_', '')
    # STT
    if cl in ('stt', 'no', '#') or cl_nospace == 'stt':
      return 0, 48
    # Tên nhóm
    if (
        'tênnhóm' in cl_nospace or 'tennhom' in cl_nospace
        or cl in ('tên nhóm', 'ten nhom', 'nhóm', 'nhom', 'group name')
        or (cl_nospace in ('nhóm', 'nhom', 'group'))
    ):
      return 1, 120
    # Outlet Code
    if (
        'outletcode' in cl_nospace or 'outlet_code' in cl.replace(' ', '_')
        or 'mãkh' in cl_nospace or 'makh' in cl_nospace or 'mãch' in cl_nospace
        or cl in ('outlet code', 'outlet', 'mã kh', 'ma kh', 'mã ch', 'ma ch', 'customer code')
    ):
      return 2, 110
    # Tên CH
    if (
        'tênch' in cl_nospace or 'tench' in cl_nospace
        or 'tênkh' in cl_nospace or 'tenkh' in cl_nospace
        or 'outletname' in cl_nospace or 'customername' in cl_nospace
        or cl in ('tên ch', 'ten ch', 'tên kh', 'ten kh', 'outlet name', 'tên cửa hàng')
    ):
      return 3, 170
    return None

  freeze = []  # (order, width, col)
  other = []
  seen_key = set()
  for c in selected_cols:
    fk = _freeze_key(c)
    if fk is not None:
      key, w = fk
      if key in seen_key:
        other.append(c)
        continue
      seen_key.add(key)
      freeze.append((key, w, c))
    else:
      other.append(c)
  freeze.sort(key=lambda x: x[0])
  ordered = [c for _, _, c in freeze] + other

  # left offsets
  left = 0
  widths = {}  # col -> (left, width)
  for key, w, c in freeze:
    widths[c] = (left, w)
    left += w

  sh = 'box-shadow:3px 0 5px -2px rgba(0,0,0,.2);'

  html = [
      '<div class="mbs-data-scroll">',
      '<table class="mbs-data-table" style="border-collapse:separate !important;'
      'border-spacing:0 !important;width:max-content !important;min-width:100%;">',
      '<thead><tr>',
  ]
  for col in ordered:
    if col in widths:
      L, w = widths[col]
      html.append(
          f'<th class="mbs-sticky-col" style="position:sticky !important;left:{L}px !important;'
          f'top:0 !important;z-index:12 !important;min-width:{w}px !important;'
          f'max-width:{w}px !important;background:#034ea2 !important;color:#fff !important;'
          f'{sh}">{col}</th>'
      )
    else:
      html.append(
          f'<th style="position:sticky !important;top:0 !important;z-index:4 !important;'
          f'background:#034ea2 !important;color:#fff !important;">{col}</th>'
      )
  html.append('</tr></thead><tbody>')

  for pos, (_, row) in enumerate(df_show.iterrows()):
    bg = '#f7fbff' if pos % 2 == 0 else '#ffffff'
    html.append('<tr>')
    for col in ordered:
      val = row.get(col, '')
      if pd.isna(val):
        val = ''
      sval = str(val)
      col_lower = str(col).lower()

      sticky = f'background-color:{bg} !important;'
      if col in widths:
        L, w = widths[col]
        sticky = (
            f'position:sticky !important;left:{L}px !important;z-index:8 !important;'
            f'min-width:{w}px !important;max-width:{w}px !important;'
            f'background-color:{bg} !important;{sh}'
        )

      if '%' in str(col):
        cls = color_pct_class(sval)
        style = color_pct_bg(sval)
        html.append(
            f'<td data-colored="1" class="{cls}" style="{style}{sticky}'
            f'text-align:center !important;white-space:nowrap;">{sval}</td>'
        )
      elif any(x in col_lower for x in [
          'phân loại cat', 'phan loai cat', 'loại cat',
          'phân loại brand', 'phan loai brand', 'loại brand'
      ]):
        t = sval.strip().upper()
        if t == 'OLD':
          style = 'background:#edf2f7 !important;color:#4a5568 !important;font-weight:700 !important;'
        elif t == 'NEW':
          style = 'background:#fefcbf !important;color:#744210 !important;font-weight:800 !important;'
        elif t == 'FOCUS':
          style = 'background:#c6f6d5 !important;color:#22543d !important;font-weight:800 !important;'
        else:
          style = ''
        html.append(
            f'<td data-colored="1" style="{style}{sticky}text-align:center !important;'
            f'white-space:nowrap;">{sval}</td>'
        )
      else:
        align = 'left' if any(
            x in col_lower for x in ['name', 'tên', 'sm name', 'nhóm', 'nhom', 'ch']
        ) else 'center'
        if 'doanh số' in col_lower or 'doanhso' in col_lower.replace(' ', '') or 'điểm thưởng' in col_lower:
          align = 'right'
        if col in widths:
          key = next((k for k, w, c in freeze if c == col), None)
          align = 'center' if key == 0 else 'left'
        html.append(
            f'<td style="{sticky}text-align:{align} !important;white-space:nowrap;'
            f'overflow:hidden;text-overflow:ellipsis;">{sval}</td>'
        )
    html.append('</tr>')

  html.append('</tbody></table></div>')
  st.markdown(''.join(html), unsafe_allow_html=True)







st.markdown(
    """
    <style>
    /* MBS CAT / BRAND: chỉ format màu, giữ nguyên scroll/kích thước */
    .mbs-summary-scroll,
    .mbs-data-scroll {
      width: 100%;
      /* Tối đa ~15 dòng: vẫn giữ cuộn dọc + cuộn ngang */
      max-height: 480px;
      overflow-x: auto !important;
      overflow-y: auto !important;
      -webkit-overflow-scrolling: touch;
      border: 1px solid #9ca3af;
    }
    .mbs-summary-table,
    .mbs-data-table {
      border-collapse: collapse !important;
      font-size: 11px !important;
      border: 1px solid #9ca3af !important;
      /* Tự scale theo khung: ít cột thì full khung, nhiều cột thì tự rộng để cuộn ngang */
      width: max-content !important;
      min-width: 100% !important;
      table-layout: auto !important;
      margin: 0 !important;
    }
    .mbs-summary-table thead th,
    .mbs-data-table thead th {
      position: sticky;
      top: 0;
      z-index: 4;
    }
    .mbs-data-table th.mbs-sticky-col {
      position: sticky !important;
      z-index: 12 !important;
      background: #034ea2 !important;
    }
    .mbs-data-table td {
      background-clip: padding-box;
    }
    .mbs-summary-table th,
    .mbs-data-table th {
      background: #034ea2 !important;
      color: #ffffff !important;
      font-weight: 800 !important;
      text-align: center !important;
      border: 1px solid #ffffff !important;
      padding: 5px 7px !important;
      white-space: nowrap !important;
    }
    .mbs-summary-table td,
    .mbs-data-table td {
      border: 1px solid #d1d5db !important;
      padding: 4px 7px !important;
      white-space: nowrap !important;
    }
    .mbs-summary-table tbody tr:nth-child(even),
    .mbs-data-table tbody tr:nth-child(even) {
      background: #f7fbff !important;
    }
    .mbs-summary-table tbody tr:nth-child(odd),
    .mbs-data-table tbody tr:nth-child(odd) {
      background: #ffffff !important;
    }
    .mbs-summary-table tbody tr:hover,
    .mbs-data-table tbody tr:hover {
      background: #eaf3ff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def render_mbs_data_summary(df_summary, title):
  """Render bảng Summary MBS: format màu + cuộn ngang/dọc, tối đa ~15 dòng."""
  if df_summary is None or df_summary.empty:
    st.info(f'Không có dữ liệu {title} phù hợp bộ lọc hiện tại.')
    return

  df_show = df_summary.copy()
  money_cols = [
      'Chỉ tiêu doanh số',
      'Doanh số thực hiện (Paid & Invoiced)',
      'Doanh số thực hiện ( Not Cancel/Pending)',
  ]
  for c in money_cols:
    if c in df_show.columns:
      df_show[c] = pd.to_numeric(df_show[c], errors='coerce').fillna(0).apply(format_number_vn)
  if '% Th/CT (Paid & Invoiced)' in df_show.columns:
    df_show['% Th/CT (Paid & Invoiced)'] = df_show['% Th/CT (Paid & Invoiced)'].apply(
        lambda x: f'{float(x):.1f}%'
    )
  if 'Điểm thưởng dự kiến' in df_show.columns:
    df_show['Điểm thưởng dự kiến'] = pd.to_numeric(
        df_show['Điểm thưởng dự kiến'], errors='coerce'
    ).fillna(0).apply(lambda x: f'{float(x):,.0f}'.replace(',', '.'))

  st.markdown(
      f'<p style="font-weight:800; color:#034ea2; margin:14px 0 6px 0;">'
      f'📊 {title}</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p style="font-size:11.5px; color:#4a5568; margin:0 0 6px 0;">'
      'OLD = Cũ &nbsp;|&nbsp; NEW = Mới &nbsp;|&nbsp; FOCUS = Duy trì &nbsp;|&nbsp; '
      'Cần duy trì = tất cả FOCUS &nbsp;|&nbsp; Đã mua = FOCUS/NEW có DS ≥ 200.000 &nbsp;|&nbsp; '
      'Doanh số lấy từ RPT_061.</p>',
      unsafe_allow_html=True,
  )

  # Render HTML để format màu giống bảng KPI, đồng thời giữ cuộn ngang + dọc.
  html = [
      '<div class="mbs-summary-scroll">',
      '<table class="mbs-summary-table">',
      '<thead><tr>',
  ]
  for col in df_show.columns:
    html.append(f'<th>{col}</th>')
  html.append('</tr></thead><tbody>')

  for _, row in df_show.iterrows():
    html.append('<tr>')
    for col in df_show.columns:
      val = row.get(col, '')
      if pd.isna(val):
        val = ''
      sval = str(val)
      col_lower = str(col).lower()

      if '%' in str(col):
        cls = color_pct_class(sval)
        style = color_pct_bg(sval)
        html.append(
            f'<td data-colored="1" class="{cls}" style="{style}'
            'text-align:center !important;white-space:nowrap;">'
            f'{sval}</td>'
        )
      elif 'điểm thưởng dự kiến' in col_lower:
        html.append(
            '<td style="text-align:center !important;'
            'background:#fff7ed !important;color:#9a3412 !important;'
            'font-weight:800 !important;white-space:nowrap;">'
            f'{sval}</td>'
        )
      elif any(x in col_lower for x in ['doanh số', 'doanhso', 'chỉ tiêu']):
        html.append(
            '<td style="text-align:right !important;white-space:nowrap;">'
            f'{sval}</td>'
        )
      elif any(x in col_lower for x in ['sm name', 'sm uid', 'outlet name', 'outlet code']):
        align = 'left' if 'name' in col_lower else 'center'
        html.append(
            f'<td style="text-align:{align} !important;white-space:nowrap;">'
            f'{sval}</td>'
        )
      else:
        html.append(
            '<td style="text-align:center !important;white-space:nowrap;">'
            f'{sval}</td>'
        )
    html.append('</tr>')

  html.append('</tbody></table></div>')
  st.markdown(''.join(html), unsafe_allow_html=True)
  st.caption(f'Tổng: {len(df_show):,} cửa hàng | Hiển thị theo bộ lọc hiện tại')



# ----- TAB MCP -----


with tab_mcp:
  st.markdown(
      '<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px;'
      ' font-size: 15px;">🗺️ MCP VISIT & MAPPING DOANH SỐ BÁN HÀNG</h3>',
      unsafe_allow_html=True,
  )
  if mcp.empty:
    st.warning('Chưa có dữ liệu MCP')
  else:
    col_nv = find_col(
        mcp,
        [
            'SM name',
            'SM Name',
            'Tên NVBH',
            'Nhân viên',
            'Sale name',
            'Position name',
        ],
    )
    col_ma = find_col(
        mcp, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã khách hàng', 'Poscode']
    )
    col_ten = find_col(
        mcp, ['Outlet_name', 'Outlet Name', 'Tên CH', 'Tên khách hàng']
    )
    col_thu = find_col(mcp, ['Thứ', 'Frequency', 'Tần suất'])
    col_vip = find_col(mcp, ['VIP MCH', 'VIP_MCH'])
    col_l1 = find_col(mcp, ['L1', 'Channel', 'Kênh', 'x_msc_business_type_l1'])
    col_ds = find_col(
        mcp, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD']
    )

    saved_mcp_nv = st.query_params.get('mcp_nv', '')
    default_nv_list = (
        [x.strip() for x in saved_mcp_nv.split(',') if x.strip()]
        if saved_mcp_nv
        else []
    )

    saved_mcp_thu = st.query_params.get('mcp_thu', '')
    default_thu_list = (
        [x.strip() for x in saved_mcp_thu.split(',') if x.strip()]
        if saved_mcp_thu
        else []
    )

    saved_mcp_ma = st.query_params.get('mcp_ma', '')
    saved_mcp_ten = st.query_params.get('mcp_ten', '')

    saved_mcp_vip = st.query_params.get('mcp_vip', '')
    default_vip_list = (
        [x.strip() for x in saved_mcp_vip.split(',') if x.strip()]
        if saved_mcp_vip
        else []
    )

    saved_mcp_l1 = st.query_params.get('mcp_l1', '')
    default_l1_list = (
        [x.strip() for x in saved_mcp_l1.split(',') if x.strip()]
        if saved_mcp_l1
        else []
    )

    saved_mcp_ds = st.query_params.get('mcp_ds', '')
    default_ds_list = (
        [x.strip() for x in saved_mcp_ds.split(',') if x.strip()]
        if saved_mcp_ds
        else []
    )

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      nv_opts = (
          sorted(mcp[col_nv].dropna().astype(str).unique().tolist())
          if col_nv
          else []
      )
      valid_default_nv = [v for v in default_nv_list if v in nv_opts]
      f_nv = st.multiselect(
          '',
          nv_opts,
          default=valid_default_nv,
          key='mcp_nv_input',
          on_change=update_mcp_params,
          label_visibility='collapsed',
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      valid_default_thu = [t for t in default_thu_list if t in thu_opts]
      f_thu = st.multiselect(
          '',
          thu_opts,
          default=valid_default_thu,
          key='mcp_thu_input',
          on_change=update_mcp_params,
          label_visibility='collapsed',
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ma = st.text_input(
          '',
          value=saved_mcp_ma,
          key='mcp_ma_input',
          on_change=update_mcp_params,
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ten = st.text_input(
          '',
          value=saved_mcp_ten,
          key='mcp_ten_input',
          on_change=update_mcp_params,
          label_visibility='collapsed',
      )

    c5, c6, c6b = st.columns(3)
    with c5:
      st.markdown(
          '<p class="filter-label">⭐ Lọc VIP MCH (Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      vip_opts = (
          sorted(mcp[col_vip].dropna().astype(str).unique().tolist())
          if col_vip
          else []
      )
      valid_default_vip = [v for v in default_vip_list if v in vip_opts]
      f_vip = st.multiselect(
          '',
          vip_opts,
          default=valid_default_vip,
          key='mcp_vip_input',
          on_change=update_mcp_params,
          label_visibility='collapsed',
      )
    with c6:
      st.markdown(
          '<p class="filter-label">🏬 Lọc L1 (Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      l1_opts = (
          sorted(mcp[col_l1].dropna().astype(str).unique().tolist())
          if col_l1
          else []
      )
      valid_default_l1 = [v for v in default_l1_list if v in l1_opts]
      f_l1 = st.multiselect(
          '',
          l1_opts,
          default=valid_default_l1,
          key='mcp_l1_input',
          on_change=update_mcp_params,
          label_visibility='collapsed',
      )
    with c6b:
      st.markdown(
          '<p class="filter-label">💰 Lọc Doanh Số MTD Thực Tế (Chọn'
          ' nhiều)</p>',
          unsafe_allow_html=True,
      )
      if col_ds:
        raw_ds_vals = sorted(mcp[col_ds].dropna().unique().tolist())
        ds_opts = [format_number_vn(v) for v in raw_ds_vals]
      else:
        ds_opts = []
      valid_default_ds = [d for d in default_ds_list if d in ds_opts]
      f_ds = st.multiselect(
          '',
          ds_opts,
          default=valid_default_ds,
          key='mcp_ds_input',
          on_change=update_mcp_params,
          label_visibility='collapsed',
      )

    st.query_params['mcp_nv'] = (
        ','.join(st.session_state.mcp_nv_input)
        if st.session_state.mcp_nv_input
        else ''
    )
    st.query_params['mcp_thu'] = (
        ','.join(st.session_state.mcp_thu_input)
        if st.session_state.mcp_thu_input
        else ''
    )
    st.query_params['mcp_ma'] = st.session_state.mcp_ma_input
    st.query_params['mcp_ten'] = st.session_state.mcp_ten_input
    st.query_params['mcp_vip'] = (
        ','.join(st.session_state.mcp_vip_input)
        if st.session_state.mcp_vip_input
        else ''
    )
    st.query_params['mcp_l1'] = (
        ','.join(st.session_state.mcp_l1_input)
        if st.session_state.get('mcp_l1_input')
        else ''
    )
    st.query_params['mcp_ds'] = (
        ','.join(st.session_state.mcp_ds_input)
        if st.session_state.mcp_ds_input
        else ''
    )

    # ===== MCP: chuẩn bị data + lọc (tất cả bộ lọc nằm TRÊN 2 bảng) =====
    df_total = mcp.copy()
    d_nv = col_nv
    d_ma = col_ma
    d_ten = col_ten
    d_thu = col_thu
    d_vip = col_vip
    d_ds = col_ds if col_ds and col_ds in df_total.columns else find_col(
        df_total, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD']
    )

    def _apply_mcp_base_filters(df0):
      dfx = df0.copy()
      if dfx.empty:
        return dfx
      if f_nv and d_nv and d_nv in dfx.columns:
        dfx = dfx[dfx[d_nv].astype(str).isin(f_nv)]
      if f_ma and d_ma and d_ma in dfx.columns:
        dfx = dfx[dfx[d_ma].astype(str).str.contains(f_ma, case=False, na=False)]
      if f_ten and d_ten and d_ten in dfx.columns:
        dfx = dfx[dfx[d_ten].astype(str).str.contains(f_ten, case=False, na=False)]
      if f_vip and d_vip and d_vip in dfx.columns:
        dfx = dfx[dfx[d_vip].astype(str).isin(f_vip)]
      if f_l1 and col_l1 and col_l1 in dfx.columns:
        dfx = dfx[dfx[col_l1].astype(str).isin(f_l1)]
      if d_thu and d_thu in dfx.columns:
        dfx = filter_by_thu_multi(dfx, d_thu, f_thu)
      if f_ds and d_ds and d_ds in dfx.columns:
        formatted_col_ds = pd.to_numeric(dfx[d_ds], errors='coerce').apply(format_number_vn).astype(str)
        dfx = dfx[formatted_col_ds.isin(f_ds)]
      return dfx

    try:
      df_detail = build_mcp_sales_detail(df, mcp, report_date=report_date)
    except Exception:
      df_detail = pd.DataFrame()
    if df_detail is None or df_detail.empty:
      df_detail = mcp.copy()

    d_ds_detail = d_ds if d_ds and d_ds in df_detail.columns else find_col(
        df_detail, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD']
    )

    # Base filter cho cả 2 bảng
    df_total_f = _apply_mcp_base_filters(df_total)
    df_f = _apply_mcp_base_filters(df_detail)

    # Bộ lọc SP (chung, nằm trên cả 2 bảng)
    sub_opts = sorted([
        x for x in df_f['Sub Division'].dropna().astype(str).unique().tolist()
        if x and x.lower() not in ('nan', 'none', '')
    ]) if 'Sub Division' in df_f.columns else []
    grp_opts = sorted([
        x for x in df_f['Group STD SKU'].dropna().astype(str).unique().tolist()
        if x and x.lower() not in ('nan', 'none', '')
    ]) if 'Group STD SKU' in df_f.columns else []
    sp_opts = sorted([
        x for x in df_f['Tên sản phẩm'].dropna().astype(str).unique().tolist()
        if x and x.lower() not in ('nan', 'none', '')
    ]) if 'Tên sản phẩm' in df_f.columns else []

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
      st.markdown(
          '<p class="filter-label">📂 Lọc Sub Division</p>',
          unsafe_allow_html=True,
      )
      f_sub = st.multiselect(
          '', sub_opts, default=[], key='mcp_sub_input',
          placeholder='Tất cả Sub Division', label_visibility='collapsed',
      )
    with fc2:
      st.markdown(
          '<p class="filter-label">📦 Lọc Group STD SKU</p>',
          unsafe_allow_html=True,
      )
      if f_sub and 'Sub Division' in df_f.columns and 'Group STD SKU' in df_f.columns:
        grp_opts_f = sorted([
            x for x in df_f[df_f['Sub Division'].astype(str).isin(f_sub)]['Group STD SKU']
            .dropna().astype(str).unique().tolist()
            if x and x.lower() not in ('nan', 'none', '')
        ])
      else:
        grp_opts_f = grp_opts
      f_grp = st.multiselect(
          '', grp_opts_f, default=[], key='mcp_grp_input',
          placeholder='Tất cả Group STD', label_visibility='collapsed',
      )
    with fc3:
      st.markdown(
          '<p class="filter-label">🏷️ Lọc Tên sản phẩm</p>',
          unsafe_allow_html=True,
      )
      _tmp = df_f
      if f_sub and 'Sub Division' in _tmp.columns:
        _tmp = _tmp[_tmp['Sub Division'].astype(str).isin(f_sub)]
      if f_grp and 'Group STD SKU' in _tmp.columns:
        _tmp = _tmp[_tmp['Group STD SKU'].astype(str).isin(f_grp)]
      if 'Tên sản phẩm' in _tmp.columns:
        sp_opts_f = sorted([
            x for x in _tmp['Tên sản phẩm'].dropna().astype(str).unique().tolist()
            if x and x.lower() not in ('nan', 'none', '')
        ])
      else:
        sp_opts_f = sp_opts
      f_sp = st.multiselect(
          '', sp_opts_f, default=[], key='mcp_sp_input',
          placeholder='Tất cả Tên SP', label_visibility='collapsed',
      )

    # SP filters áp vào bảng chi tiết
    has_sp_filter = bool(f_sub or f_grp or f_sp)
    if f_sub and 'Sub Division' in df_f.columns:
      df_f = df_f[df_f['Sub Division'].astype(str).isin(f_sub)]
    if f_grp and 'Group STD SKU' in df_f.columns:
      df_f = df_f[df_f['Group STD SKU'].astype(str).isin(f_grp)]
    if f_sp and 'Tên sản phẩm' in df_f.columns:
      df_f = df_f[df_f['Tên sản phẩm'].astype(str).isin(f_sp)]

    # ===== BẢNG 0: Tổng hợp theo Nhân Viên =====
    try:
      _perf_raw = load_perf_sku_data()
    except Exception:
      _perf_raw = pd.DataFrame()
    try:
      df_nv_sum = build_mcp_nv_summary(
          df_total_f,
          df_f,
          filter_nv=f_nv if f_nv else None,
          f_sub=f_sub,
          f_grp=f_grp,
          f_sp=f_sp,
          report_date=report_date,
          df_perf_raw=_perf_raw,
          df_rpt=df,
      )
    except Exception as e:
      df_nv_sum = pd.DataFrame()
      st.caption(f'(Lỗi tổng hợp NV MCP: {e})')

    st.markdown(
        '<p style="font-weight:800;color:#034ea2;margin:10px 0 4px;">'
        '0. TỔNG HỢP THEO NHÂN VIÊN — CHỈ TIÊU / MTD / MCP / ASO</p>',
        unsafe_allow_html=True,
    )
    if df_nv_sum is None or df_nv_sum.empty:
      st.info('Không có dữ liệu tổng hợp theo nhân viên.')
    else:
      cols_nv = [
          'STT', 'Tên NVBH', 'Chỉ tiêu Doanh Số', 'MTD', '% MTD DS',
          'MCP', 'ASO', '% MTD ASO/MCP',
      ]
      _html = [
          '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">',
          '<table class="custom-kpi-table">',
          '<thead><tr>',
      ]
      for _c in cols_nv:
        _html.append(f'<th>{_c}</th>')
      _html.append('</tr></thead><tbody>')
      _sum = {
          'Chỉ tiêu Doanh Số': 0.0, 'MTD': 0.0,
          'MCP': 0, 'ASO': 0,
      }
      for _i, (_, _row) in enumerate(df_nv_sum[cols_nv].iterrows()):
        _bg = '#e6f7ff' if _i % 2 == 0 else '#ffffff'
        _html.append(f'<tr style="background-color:{_bg} !important;">')
        for _c in cols_nv:
          _v = _row.get(_c, '')
          if pd.isna(_v):
            _v = ''
          if _c in ('Chỉ tiêu Doanh Số', 'MTD'):
            try:
              _num = float(_v) if _v != '' else 0.0
            except Exception:
              _num = 0.0
            _sum[_c] = _sum.get(_c, 0) + _num
            _s = format_number_vn(_num)
            _html.append(
                f'<td style="text-align:right;background-color:{_bg} !important;">{_s}</td>'
            )
          elif _c in ('MCP', 'ASO'):
            try:
              _num = int(float(_v)) if _v != '' else 0
            except Exception:
              _num = 0
            _sum[_c] = _sum.get(_c, 0) + _num
            _html.append(
                f'<td style="text-align:center;background-color:{_bg} !important;">{_num}</td>'
            )
          elif _c in ('% MTD DS', '% MTD ASO/MCP'):
            try:
              _pct = float(_v) if _v != '' else 0.0
            except Exception:
              _pct = 0.0
            _s = f'{_pct:.1f}%'.rstrip('0').rstrip('.').replace('.0', '') if False else f'{_pct}%'
            # color theo timegone rule
            try:
              _cls = color_pct_class(f'{_pct}%')
              _sty = color_pct_bg(f'{_pct}%')
            except Exception:
              _cls, _sty = '', ''
            _html.append(
                f'<td data-colored="1" class="{_cls}" style="text-align:center;'
                f'background-color:{_bg} !important;{_sty}">{_pct}%</td>'
            )
          elif _c == 'Tên NVBH':
            _html.append(
                f'<td style="text-align:left;background-color:{_bg} !important;">{_v}</td>'
            )
          else:
            _html.append(
                f'<td style="text-align:center;background-color:{_bg} !important;">{_v}</td>'
            )
        _html.append('</tr>')
      # Total
      _tot_bg = '#1a365d'
      _pct_ds_tot = (
          round(_sum['MTD'] / _sum['Chỉ tiêu Doanh Số'] * 100, 1)
          if _sum['Chỉ tiêu Doanh Số'] > 0 else 0.0
      )
      _pct_aso_tot = (
          round(_sum['ASO'] / _sum['MCP'] * 100, 1)
          if _sum['MCP'] > 0 else 0.0
      )
      _html.append(f'<tr style="background-color:{_tot_bg} !important;">')
      for _c in cols_nv:
        if _c == 'STT':
          _s = ''
        elif _c == 'Tên NVBH':
          _s = 'TỔNG CỘNG'
        elif _c in ('Chỉ tiêu Doanh Số', 'MTD'):
          _s = format_number_vn(_sum[_c])
        elif _c == 'MCP':
          _s = str(_sum['MCP'])
        elif _c == 'ASO':
          _s = str(_sum['ASO'])
        elif _c == '% MTD DS':
          _s = f'{_pct_ds_tot}%'
        elif _c == '% MTD ASO/MCP':
          _s = f'{_pct_aso_tot}%'
        else:
          _s = ''
        if _c in ('% MTD DS', '% MTD ASO/MCP'):
          try:
            _cls = color_pct_class(_s)
            _sty = color_pct_bg(_s)
          except Exception:
            _cls, _sty = '', ''
          _html.append(
              f'<td data-colored="1" class="{_cls}" style="text-align:center;'
              f'background-color:{_tot_bg} !important;color:#ffffff !important;'
              f'font-weight:800 !important;{_sty}">{_s}</td>'
          )
        else:
          _html.append(
              f'<td style="text-align:{"right" if _c in ("Chỉ tiêu Doanh Số","MTD") else "center"};'
              f'background-color:{_tot_bg} !important;color:#ffffff !important;'
              f'font-weight:800 !important;">{_s}</td>'
          )
      _html.append('</tr>')
      _html.append('</tbody></table></div>')
      st.markdown(''.join(_html), unsafe_allow_html=True)
      st.caption(
          f'Hiển thị: {len(df_nv_sum):,} nhân viên | '
          f'Chỉ tiêu theo Performance'
          + (' (lọc Sub/Group/SP)' if (f_sub or f_grp or f_sp) else ' (full)')
      )

    # ===== BẢNG 1: MCP gốc — DS MTD theo điều kiện lọc SP (nếu có) =====
    df_total_show = df_total_f.copy()

    # Xác định cột mã CH để map DS từ chi tiết
    _ma_total = d_ma if d_ma and d_ma in df_total_show.columns else find_col(
        df_total_show, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH']
    )
    _ma_detail = d_ma if d_ma and d_ma in df_f.columns else find_col(
        df_f, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã KH']
    )
    _ds_col_detail = d_ds_detail if d_ds_detail and d_ds_detail in df_f.columns else find_col(
        df_f, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD']
    )

    def _norm_ma_val(x):
      s = str(x).strip()
      return s[:-2] if s.endswith('.0') else s

    if has_sp_filter and _ma_detail and _ds_col_detail and not df_f.empty:
      # Tính lại DS theo Sub/Group/SP đang lọc (sum theo Mã KH)
      _tmp = df_f[[_ma_detail, _ds_col_detail]].copy()
      _tmp['_ma'] = _tmp[_ma_detail].map(_norm_ma_val)
      _tmp['_ds'] = pd.to_numeric(_tmp[_ds_col_detail], errors='coerce').fillna(0)
      ds_by_ma = _tmp.groupby('_ma')['_ds'].sum().to_dict()

      if _ma_total and d_ds and d_ds in df_total_show.columns:
        df_total_show['_ma'] = df_total_show[_ma_total].map(_norm_ma_val)
        # Chỉ giữ CH có DS theo filter (hoặc DS = 0 vẫn hiện? → chỉ hiện CH có trong filter)
        df_total_show = df_total_show[df_total_show['_ma'].isin(ds_by_ma.keys())].copy()
        df_total_show[d_ds] = df_total_show['_ma'].map(ds_by_ma).fillna(0)
        df_total_show = df_total_show.drop(columns=['_ma'], errors='ignore')
      elif _ma_total:
        # không có cột DS sẵn → tạo mới
        df_total_show['_ma'] = df_total_show[_ma_total].map(_norm_ma_val)
        df_total_show = df_total_show[df_total_show['_ma'].isin(ds_by_ma.keys())].copy()
        df_total_show['Doanh Số MTD'] = df_total_show['_ma'].map(ds_by_ma).fillna(0)
        df_total_show = df_total_show.drop(columns=['_ma'], errors='ignore')
        d_ds = 'Doanh Số MTD'
    # else: giữ DS total gốc (không lọc SP)

    # format DS sau khi đã tính lại
    if d_ds and d_ds in df_total_show.columns:
      df_total_show[d_ds] = pd.to_numeric(
          df_total_show[d_ds], errors='coerce'
      ).apply(format_number_vn)

    total_all_cols = [c for c in list(mcp.columns) if c in df_total_show.columns]
    if d_ds and d_ds in df_total_show.columns and d_ds not in total_all_cols:
      total_all_cols.append(d_ds)

    saved_mcp_total_cols = st.query_params.get('mcp_total_cols', None)
    default_total_cols = total_all_cols
    if saved_mcp_total_cols:
      if isinstance(saved_mcp_total_cols, str):
        saved_t = [c.strip() for c in saved_mcp_total_cols.split(',') if c.strip() in total_all_cols]
      else:
        saved_t = [c for c in saved_mcp_total_cols if c in total_all_cols]
      if saved_t and len(saved_t) >= max(3, int(len(total_all_cols) * 0.4)):
        default_total_cols = saved_t

    st.markdown(
        '<p style="font-weight:800;color:#034ea2;margin:10px 0 4px;">'
        '1. DATA MCP GỐC — DOANH SỐ MTD TOTAL (theo cửa hàng)</p>',
        unsafe_allow_html=True,
    )
    with st.popover('👁️ Chọn cột hiển thị (MCP Gốc)', use_container_width=False):
      selected_total_cols = st.multiselect(
          'Bỏ chọn để ẩn cột:',
          total_all_cols,
          default=default_total_cols,
          key='mcp_total_cols_input',
      )
    st.query_params['mcp_total_cols'] = ','.join(selected_total_cols)
    if not selected_total_cols:
      selected_total_cols = total_all_cols
    render_mbs_data_table(df_total_show, selected_total_cols)
    _cap_ds = (
        'Doanh Số MTD theo bộ lọc Sub/Group/SP'
        if has_sp_filter else
        'Doanh Số MTD = tổng từ đầu tháng đến ngày BC'
    )
    st.caption(
        f'Hiển thị: {len(df_total_show):,} / {len(mcp):,} cửa hàng | {_cap_ds}'
    )

    # ===== BẢNG 2: Chi tiết DS theo Sub / Group / SP =====
    df_show = df_f.copy()
    if d_ds_detail and d_ds_detail in df_show.columns:
      df_show[d_ds_detail] = pd.to_numeric(
          df_show[d_ds_detail], errors='coerce'
      ).apply(format_number_vn)
    elif 'Doanh Số MTD' in df_show.columns:
      df_show['Doanh Số MTD'] = pd.to_numeric(
          df_show['Doanh Số MTD'], errors='coerce'
      ).apply(format_number_vn)

    detail_cols = ['Sub Division', 'Group STD SKU', 'Tên sản phẩm']
    preferred = []
    for c in list(mcp.columns) + detail_cols:
      if c in df_show.columns and c not in preferred:
        preferred.append(c)
    all_cols_mcp = preferred + [c for c in df_show.columns if c not in preferred]
    saved_mcp_cols = st.query_params.get('mcp_cols', None)
    default_cols_mcp = all_cols_mcp
    if saved_mcp_cols:
      if isinstance(saved_mcp_cols, str):
        saved_list = [c.strip() for c in saved_mcp_cols.split(',') if c.strip() in all_cols_mcp]
      else:
        saved_list = [c for c in saved_mcp_cols if c in all_cols_mcp]
      if saved_list and len(saved_list) >= max(5, int(len(all_cols_mcp) * 0.5)):
        default_cols_mcp = saved_list

    st.markdown(
        '<p style="font-weight:800;color:#034ea2;margin:16px 0 4px;">'
        '2. DOANH SỐ MTD CHI TIẾT — Sub Division / Group STD SKU / Tên sản phẩm</p>',
        unsafe_allow_html=True,
    )
    with st.popover('👁️ Chọn cột hiển thị (Chi tiết SP)', use_container_width=False):
      selected_mcp_cols = st.multiselect(
          'Bỏ chọn để ẩn cột:',
          all_cols_mcp,
          default=default_cols_mcp,
          key='mcp_cols_input',
      )
    st.query_params['mcp_cols'] = ','.join(selected_mcp_cols)
    if not selected_mcp_cols:
      selected_mcp_cols = all_cols_mcp
    render_mbs_data_table(df_show, selected_mcp_cols)
    _ma_col = col_ma if col_ma and col_ma in df_f.columns else (
        'Mã CH' if 'Mã CH' in df_f.columns else None
    )
    n_kh = df_f[_ma_col].nunique() if _ma_col else len(df_f)
    st.caption(
        f'Hiển thị: {len(df_f):,} dòng SP / {n_kh:,} cửa hàng'
        f' (tổng MCP: {len(mcp):,} CH)'
    )



# ----- TAB CAT -----
with tab_cat:
  st.markdown(
      '<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px;'
      ' font-size: 15px;">🎯 TRACKING MBS - THEO NGÀNH HÀNG (CATEGORY)</h3>',
      unsafe_allow_html=True,
  )
  if df_cat.empty:
    st.error("❌ Không tìm thấy Data_Cat.xlsx trong thư mục 'data'")
  else:
    col_nv = find_col(df_cat, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    col_ma = find_col(df_cat, ['Outlet Code', 'Outlet_code', 'Mã CH', 'Mã khách hàng'])
    col_ten = find_col(df_cat, ['Outlet Name', 'Outlet_name', 'Tên CH', 'Tên khách hàng'])
    col_thu = find_col(df_cat, ['Thứ'])

    saved_cat_nv = st.query_params.get('cat_nv', '')
    default_cat_nv_list = (
        [x.strip() for x in saved_cat_nv.split(',') if x.strip()]
        if saved_cat_nv
        else []
    )

    saved_cat_thu = st.query_params.get('cat_thu', '')
    default_cat_thu_list = (
        [x.strip() for x in saved_cat_thu.split(',') if x.strip()]
        if saved_cat_thu
        else []
    )

    saved_cat_ma = st.query_params.get('cat_ma', '')
    saved_cat_ten = st.query_params.get('cat_ten', '')

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      nv_opts = (
          sorted(df_cat[col_nv].dropna().astype(str).unique().tolist())
          if col_nv
          else []
      )
      valid_cat_nv = [v for v in default_cat_nv_list if v in nv_opts]
      f_nv = st.multiselect(
          '',
          nv_opts,
          default=valid_cat_nv,
          key='cat_nv_input',
          on_change=update_cat_params,
          label_visibility='collapsed',
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      valid_cat_thu = [t for t in default_cat_thu_list if t in thu_opts]
      f_thu = st.multiselect(
          '',
          thu_opts,
          default=valid_cat_thu,
          key='cat_thu_input',
          on_change=update_cat_params,
          label_visibility='collapsed',
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ma = st.text_input(
          '',
          value=saved_cat_ma,
          key='cat_ma_input',
          on_change=update_cat_params,
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ten = st.text_input(
          '',
          value=saved_cat_ten,
          key='cat_ten_input',
          on_change=update_cat_params,
          label_visibility='collapsed',
      )

    st.query_params['cat_nv'] = (
        ','.join(st.session_state.cat_nv_input)
        if st.session_state.cat_nv_input
        else ''
    )
    st.query_params['cat_thu'] = (
        ','.join(st.session_state.cat_thu_input)
        if st.session_state.cat_thu_input
        else ''
    )
    st.query_params['cat_ma'] = st.session_state.cat_ma_input
    st.query_params['cat_ten'] = st.session_state.cat_ten_input

    df_f = df_cat.copy()
    if f_nv and col_nv:
      df_f = df_f[df_f[col_nv].astype(str).isin(f_nv)]
    if f_ma and col_ma:
      df_f = df_f[
          df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)
      ]
    if f_ten and col_ten:
      df_f = df_f[
          df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)
      ]
    df_f = filter_by_thu_multi(df_f, col_thu, f_thu)
    df_cat_summary = build_mbs_data_summary(df_f, 'CAT')
    for col in df_f.columns:
      if 'doanh số' in col.lower() or 'doanhso' in col.lower().replace(
          ' ', ''
      ):
        df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(
            format_number_vn
        )

    all_cols_cat = df_f.columns.tolist()
    saved_cat_cols = st.query_params.get('cat_cols', None)
    if saved_cat_cols:
      if isinstance(saved_cat_cols, str):
        default_cols_cat = [
            c.strip()
            for c in saved_cat_cols.split(',')
            if c.strip() in all_cols_cat
        ]
      else:
        default_cols_cat = [c for c in saved_cat_cols if c in all_cols_cat]
      if not default_cols_cat:
        default_cols_cat = all_cols_cat
    else:
      default_cols_cat = all_cols_cat

    with st.popover('👁️ Chọn cột hiển thị (Category)', use_container_width=False):
      selected_cat_cols = st.multiselect(
          'Bỏ chọn để ẩn cột:',
          all_cols_cat,
          default=default_cols_cat,
          key='cat_cols_input',
      )
    st.query_params['cat_cols'] = ','.join(selected_cat_cols)

    render_mbs_data_table(df_f, selected_cat_cols)
    st.caption(f'Hiển thị: {len(df_f):,} / {len(df_cat):,} dòng')

    render_mbs_data_summary(df_cat_summary, 'DATA_CAT SUMMARY')

# ----- TAB BRAND -----
with tab_brand:
  st.markdown(
      '<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px;'
      ' font-size: 15px;">🏷️ TRACKING MBS - THEO THƯƠNG HIỆU (BRAND)</h3>',
      unsafe_allow_html=True,
  )
  if df_brand.empty:
    st.error("❌ Không tìm thấy Data_Brand.xlsx trong thư mục 'data'")
  else:
    col_nv = find_col(df_brand, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
    col_ma = find_col(df_brand, ['Outlet Code', 'Outlet_code', 'Mã CH', 'Mã khách hàng'])
    col_ten = find_col(df_brand, ['Outlet Name', 'Outlet_name', 'Tên CH', 'Tên khách hàng'])
    col_thu = find_col(df_brand, ['Thứ'])

    saved_brand_nv = st.query_params.get('brand_nv', '')
    default_brand_nv_list = (
        [x.strip() for x in saved_brand_nv.split(',') if x.strip()]
        if saved_brand_nv
        else []
    )

    saved_brand_thu = st.query_params.get('brand_thu', '')
    default_brand_thu_list = (
        [x.strip() for x in saved_brand_thu.split(',') if x.strip()]
        if saved_brand_thu
        else []
    )

    saved_brand_ma = st.query_params.get('brand_ma', '')
    saved_brand_ten = st.query_params.get('brand_ten', '')

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      nv_opts = (
          sorted(df_brand[col_nv].dropna().astype(str).unique().tolist())
          if col_nv
          else []
      )
      valid_brand_nv = [v for v in default_brand_nv_list if v in nv_opts]
      f_nv = st.multiselect(
          '',
          nv_opts,
          default=valid_brand_nv,
          key='brand_nv_input',
          on_change=update_brand_params,
          label_visibility='collapsed',
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      valid_brand_thu = [t for t in default_brand_thu_list if t in thu_opts]
      f_thu = st.multiselect(
          '',
          thu_opts,
          default=valid_brand_thu,
          key='brand_thu_input',
          on_change=update_brand_params,
          label_visibility='collapsed',
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ma = st.text_input(
          '',
          value=saved_brand_ma,
          key='brand_ma_input',
          on_change=update_brand_params,
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ten = st.text_input(
          '',
          value=saved_brand_ten,
          key='brand_ten_input',
          on_change=update_brand_params,
          label_visibility='collapsed',
      )

    st.query_params['brand_nv'] = (
        ','.join(st.session_state.brand_nv_input)
        if st.session_state.brand_nv_input
        else ''
    )
    st.query_params['brand_thu'] = (
        ','.join(st.session_state.brand_thu_input)
        if st.session_state.brand_thu_input
        else ''
    )
    st.query_params['brand_ma'] = st.session_state.brand_ma_input
    st.query_params['brand_ten'] = st.session_state.brand_ten_input

    df_f = df_brand.copy()
    if f_nv and col_nv:
      df_f = df_f[df_f[col_nv].astype(str).isin(f_nv)]
    if f_ma and col_ma:
      df_f = df_f[
          df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)
      ]
    if f_ten and col_ten:
      df_f = df_f[
          df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)
      ]
    df_f = filter_by_thu_multi(df_f, col_thu, f_thu)
    df_brand_summary = build_mbs_data_summary(df_f, 'BRAND')
    for col in df_f.columns:
      if 'doanh số' in col.lower() or 'doanhso' in col.lower().replace(
          ' ', ''
      ):
        df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(
            format_number_vn
        )

    all_cols_brand = df_f.columns.tolist()
    saved_brand_cols = st.query_params.get('brand_cols', None)
    if saved_brand_cols:
      if isinstance(saved_brand_cols, str):
        default_cols_brand = [
            c.strip()
            for c in saved_brand_cols.split(',')
            if c.strip() in all_cols_brand
        ]
      else:
        default_cols_brand = [c for c in saved_brand_cols if c in all_cols_brand]
      if not default_cols_brand:
        default_cols_brand = all_cols_brand
    else:
      default_cols_brand = all_cols_brand

    with st.popover('👁️ Chọn cột hiển thị (Brand)', use_container_width=False):
      selected_brand_cols = st.multiselect(
          'Bỏ chọn để ẩn cột:',
          all_cols_brand,
          default=default_cols_brand,
          key='brand_cols_input',
      )
    st.query_params['brand_cols'] = ','.join(selected_brand_cols)

    render_mbs_data_table(df_f, selected_brand_cols)
    st.caption(f'Hiển thị: {len(df_f):,} / {len(df_brand):,} dòng')

    render_mbs_data_summary(df_brand_summary, 'DATA_BRAND SUMMARY')

# ----- TAB DSKH_Combo OFF -----
with tab_dskh_off:
  st.markdown(
      '<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px;'
      ' font-size: 15px;">📋 DANH SÁCH KHÁCH HÀNG COMBO OFF (TÂN_COMBO KÊNH'
      ' OFF)</h3>',
      unsafe_allow_html=True,
  )
  if df_combo_off.empty:
    st.warning("Chưa có dữ liệu Combo OFF trong thư mục 'data'")
  else:
    col_nv_off = find_col(df_combo_off, ['Tên NV', 'SM name', 'Nhân viên'])
    col_ma_off = find_col(df_combo_off, ['outlet_code', 'Outlet Code', 'Mã CH'])
    col_ten_off = find_col(df_combo_off, ['outlet_name', 'Outlet Name', 'Tên CH'])
    col_thu_off = find_col(df_combo_off, ['Thứ', 'Frequency'])

    saved_off_nv = st.query_params.get('off_nv', '')
    default_off_nv_list = (
        [x.strip() for x in saved_off_nv.split(',') if x.strip()]
        if saved_off_nv
        else []
    )

    saved_off_thu = st.query_params.get('off_thu', '')
    default_off_thu_list = (
        [x.strip() for x in saved_off_thu.split(',') if x.strip()]
        if saved_off_thu
        else []
    )

    saved_off_ma = st.query_params.get('off_ma', '')
    saved_off_ten = st.query_params.get('off_ten', '')

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      nv_opts_off = (
          sorted(df_combo_off[col_nv_off].dropna().astype(str).unique().tolist())
          if col_nv_off
          else []
      )
      valid_off_nv = [v for v in default_off_nv_list if v in nv_opts_off]
      f_off_nv = st.multiselect(
          '',
          nv_opts_off,
          default=valid_off_nv,
          key='off_nv_input',
          on_change=update_off_params,
          label_visibility='collapsed',
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      valid_off_thu = [t for t in default_off_thu_list if t in thu_opts]
      f_off_thu = st.multiselect(
          '',
          thu_opts,
          default=valid_off_thu,
          key='off_thu_input',
          on_change=update_off_params,
          label_visibility='collapsed',
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_off_ma = st.text_input(
          '',
          value=saved_off_ma,
          key='off_ma_input',
          on_change=update_off_params,
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_off_ten = st.text_input(
          '',
          value=saved_off_ten,
          key='off_ten_input',
          on_change=update_off_params,
          label_visibility='collapsed',
      )

    st.query_params['off_nv'] = (
        ','.join(st.session_state.off_nv_input)
        if st.session_state.off_nv_input
        else ''
    )
    st.query_params['off_thu'] = (
        ','.join(st.session_state.off_thu_input)
        if st.session_state.off_thu_input
        else ''
    )
    st.query_params['off_ma'] = st.session_state.off_ma_input
    st.query_params['off_ten'] = st.session_state.off_ten_input

    df_off_f = df_combo_off.copy()
    if f_off_nv and col_nv_off:
      df_off_f = df_off_f[df_off_f[col_nv_off].astype(str).isin(f_off_nv)]
    if f_off_ma and col_ma_off:
      df_off_f = df_off_f[
          df_off_f[col_ma_off]
          .astype(str)
          .str.contains(f_off_ma, case=False, na=False)
      ]
    if f_off_ten and col_ten_off:
      df_off_f = df_off_f[
          df_off_f[col_ten_off]
          .astype(str)
          .str.contains(f_off_ten, case=False, na=False)
      ]
    df_off_f = filter_by_thu_multi(df_off_f, col_thu_off, f_off_thu)

    all_cols_off = df_off_f.columns.tolist()
    saved_off_cols = st.query_params.get('off_cols', None)
    if saved_off_cols:
      if isinstance(saved_off_cols, str):
        default_cols_off = [
            c.strip()
            for c in saved_off_cols.split(',')
            if c.strip() in all_cols_off
        ]
      else:
        default_cols_off = [c for c in saved_off_cols if c in all_cols_off]
      if not default_cols_off:
        default_cols_off = all_cols_off
    else:
      default_cols_off = all_cols_off

    with st.popover('👁️ Chọn cột hiển thị (DSKH OFF)', use_container_width=False):
      selected_off_cols = st.multiselect(
          'Bỏ chọn để ẩn cột:',
          all_cols_off,
          default=default_cols_off,
          key='off_cols_input',
      )
    st.query_params['off_cols'] = ','.join(selected_off_cols)

    render_mbs_data_table(df_off_f, selected_off_cols)
    st.caption(f'Hiển thị: {len(df_off_f):,} / {len(df_combo_off):,} cửa hàng')

# ----- TAB DSKH_Combo ON -----
with tab_dskh_on:
  st.markdown(
      '<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px;'
      ' font-size: 15px;">📋 DANH SÁCH KHÁCH HÀNG COMBO ON (TÂN_COMBO KÊNH'
      ' ON)</h3>',
      unsafe_allow_html=True,
  )
  if df_combo_on.empty:
    st.warning("Chưa có dữ liệu Combo ON trong thư mục 'data'")
  else:
    col_nv_on = find_col(df_combo_on, ['Tên NV', 'SM name', 'Nhân viên'])
    col_ma_on = find_col(df_combo_on, ['outlet_code', 'Outlet Code', 'Mã CH'])
    col_ten_on = find_col(df_combo_on, ['outlet_name', 'Outlet Name', 'Tên CH'])
    col_thu_on = find_col(df_combo_on, ['Thứ', 'Frequency'])

    saved_on_nv = st.query_params.get('on_nv', '')
    default_on_nv_list = (
        [x.strip() for x in saved_on_nv.split(',') if x.strip()]
        if saved_on_nv
        else []
    )

    saved_on_thu = st.query_params.get('on_thu', '')
    default_on_thu_list = (
        [x.strip() for x in saved_on_thu.split(',') if x.strip()]
        if saved_on_thu
        else []
    )

    saved_on_ma = st.query_params.get('on_ma', '')
    saved_on_ten = st.query_params.get('on_ten', '')

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      nv_opts_on = (
          sorted(df_combo_on[col_nv_on].dropna().astype(str).unique().tolist())
          if col_nv_on
          else []
      )
      valid_on_nv = [v for v in default_on_nv_list if v in nv_opts_on]
      f_on_nv = st.multiselect(
          '',
          nv_opts_on,
          default=valid_on_nv,
          key='on_nv_input',
          on_change=update_on_params,
          label_visibility='collapsed',
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>',
          unsafe_allow_html=True,
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      valid_on_thu = [t for t in default_on_thu_list if t in thu_opts]
      f_on_thu = st.multiselect(
          '',
          thu_opts,
          default=valid_on_thu,
          key='on_thu_input',
          on_change=update_on_params,
          label_visibility='collapsed',
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_on_ma = st.text_input(
          '',
          value=saved_on_ma,
          key='on_ma_input',
          on_change=update_on_params,
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_on_ten = st.text_input(
          '',
          value=saved_on_ten,
          key='on_ten_input',
          on_change=update_on_params,
          label_visibility='collapsed',
      )

    st.query_params['on_nv'] = (
        ','.join(st.session_state.on_nv_input)
        if st.session_state.on_nv_input
        else ''
    )
    st.query_params['on_thu'] = (
        ','.join(st.session_state.on_thu_input)
        if st.session_state.on_thu_input
        else ''
    )
    st.query_params['on_ma'] = st.session_state.on_ma_input
    st.query_params['on_ten'] = st.session_state.on_ten_input

    df_on_f = df_combo_on.copy()
    if f_on_nv and col_nv_on:
      df_on_f = df_on_f[df_on_f[col_nv_on].astype(str).isin(f_on_nv)]
    if f_on_ma and col_ma_on:
      df_on_f = df_on_f[
          df_on_f[col_ma_on]
          .astype(str)
          .str.contains(f_on_ma, case=False, na=False)
      ]
    if f_on_ten and col_ten_on:
      df_on_f = df_on_f[
          df_on_f[col_ten_on]
          .astype(str)
          .str.contains(f_on_ten, case=False, na=False)
      ]
    df_on_f = filter_by_thu_multi(df_on_f, col_thu_on, f_on_thu)

    all_cols_on = df_on_f.columns.tolist()
    saved_on_cols = st.query_params.get('on_cols', None)
    if saved_on_cols:
      if isinstance(saved_on_cols, str):
        default_cols_on = [
            c.strip()
            for c in saved_on_cols.split(',')
            if c.strip() in all_cols_on
        ]
      else:
        default_cols_on = [c for c in saved_on_cols if c in all_cols_on]
      if not default_cols_on:
        default_cols_on = all_cols_on
    else:
      default_cols_on = all_cols_on

    with st.popover('👁️ Chọn cột hiển thị (DSKH ON)', use_container_width=False):
      selected_on_cols = st.multiselect(
          'Bỏ chọn để ẩn cột:',
          all_cols_on,
          default=default_cols_on,
          key='on_cols_input',
      )
    st.query_params['on_cols'] = ','.join(selected_on_cols)

    render_mbs_data_table(df_on_f, selected_on_cols)
    st.caption(f'Hiển thị: {len(df_on_f):,} / {len(df_combo_on):,} cửa hàng')
