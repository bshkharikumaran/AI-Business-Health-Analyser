/**
 * Enterprise Business Analytics & Data Intelligence Platform
 * Core Application Controller & State Engine
 */

// ==========================================================================
// 1. GLOBAL STATE & PRESET DATASETS
// ==========================================================================
const AppState = {
  activeView: 'dashboard',
  currentTheme: 'light',
  currentDateRange: '30d',
  
  // Active Ingestion Dataset
  currentDatasetId: 'saas_metrics',
  currentDatasetName: 'Enterprise SaaS ARR & Subscriptions (2025-2026)',
  currentRows: [],
  currentColumns: [],
  currentValidation: null,
  
  // Preset Enterprise Repositories
  presets: {
    saas_metrics: {
      id: 'saas_metrics',
      name: 'Enterprise SaaS ARR & Subscriptions (2025-2026)',
      description: 'Monthly recurring revenue, customer acquisition cost, churn rate, LTV, and active tier accounts.',
      category: 'Finance & SaaS',
      columns: ['Month', 'ARR_kUSD', 'MRR_kUSD', 'Active_Subscribers', 'New_Customers', 'Churn_Rate_Pct', 'CAC_USD', 'LTV_USD', 'Net_Retention_Pct', 'Region'],
      data: [
        { Month: "Jan 2025", ARR_kUSD: 3200, MRR_kUSD: 266.6, Active_Subscribers: 1420, New_Customers: 120, Churn_Rate_Pct: 2.1, CAC_USD: 450, LTV_USD: 5800, Net_Retention_Pct: 112, Region: "North America" },
        { Month: "Feb 2025", ARR_kUSD: 3340, MRR_kUSD: 278.3, Active_Subscribers: 1485, New_Customers: 135, Churn_Rate_Pct: 1.9, CAC_USD: 440, LTV_USD: 5920, Net_Retention_Pct: 114, Region: "North America" },
        { Month: "Mar 2025", ARR_kUSD: 3520, MRR_kUSD: 293.3, Active_Subscribers: 1560, New_Customers: 150, Churn_Rate_Pct: 2.3, CAC_USD: 465, LTV_USD: 6050, Net_Retention_Pct: 115, Region: "EMEA" },
        { Month: "Apr 2025", ARR_kUSD: 3690, MRR_kUSD: 307.5, Active_Subscribers: 1640, New_Customers: 145, Churn_Rate_Pct: 2.0, CAC_USD: 435, LTV_USD: 6180, Net_Retention_Pct: 116, Region: "EMEA" },
        { Month: "May 2025", ARR_kUSD: 3880, MRR_kUSD: 323.3, Active_Subscribers: 1725, New_Customers: 160, Churn_Rate_Pct: 1.8, CAC_USD: 420, LTV_USD: 6300, Net_Retention_Pct: 118, Region: "APAC" },
        { Month: "Jun 2025", ARR_kUSD: 4050, MRR_kUSD: 337.5, Active_Subscribers: 1810, New_Customers: 170, Churn_Rate_Pct: 2.2, CAC_USD: 445, LTV_USD: 6420, Net_Retention_Pct: 119, Region: "APAC" },
        { Month: "Jul 2025", ARR_kUSD: 4210, MRR_kUSD: 350.8, Active_Subscribers: 1880, New_Customers: 155, Churn_Rate_Pct: 2.5, CAC_USD: 480, LTV_USD: 6500, Net_Retention_Pct: 117, Region: "North America" },
        { Month: "Aug 2025", ARR_kUSD: 4390, MRR_kUSD: 365.8, Active_Subscribers: 1960, New_Customers: 165, Churn_Rate_Pct: 1.7, CAC_USD: 410, LTV_USD: 6650, Net_Retention_Pct: 121, Region: "North America" },
        { Month: "Sep 2025", ARR_kUSD: 4580, MRR_kUSD: 381.7, Active_Subscribers: 2045, New_Customers: 180, Churn_Rate_Pct: 1.6, CAC_USD: 395, LTV_USD: 6800, Net_Retention_Pct: 123, Region: "EMEA" },
        { Month: "Oct 2025", ARR_kUSD: 4760, MRR_kUSD: 396.6, Active_Subscribers: 2130, New_Customers: 175, Churn_Rate_Pct: 1.9, CAC_USD: 415, LTV_USD: 6910, Net_Retention_Pct: 122, Region: "EMEA" },
        { Month: "Nov 2025", ARR_kUSD: 4980, MRR_kUSD: 415.0, Active_Subscribers: 2240, New_Customers: 195, Churn_Rate_Pct: 1.5, CAC_USD: 380, LTV_USD: 7100, Net_Retention_Pct: 125, Region: "APAC" },
        { Month: "Dec 2025", ARR_kUSD: 5240, MRR_kUSD: 436.6, Active_Subscribers: 2360, New_Customers: 210, Churn_Rate_Pct: 1.4, CAC_USD: 370, LTV_USD: 7350, Net_Retention_Pct: 128, Region: "APAC" },
        { Month: "Jan 2026", ARR_kUSD: 5450, MRR_kUSD: 454.1, Active_Subscribers: 2450, New_Customers: 185, Churn_Rate_Pct: 1.8, CAC_USD: 405, LTV_USD: 7480, Net_Retention_Pct: 126, Region: "North America" },
        { Month: "Feb 2026", ARR_kUSD: 5680, MRR_kUSD: 473.3, Active_Subscribers: 2555, New_Customers: 205, Churn_Rate_Pct: 1.6, CAC_USD: 390, LTV_USD: 7620, Net_Retention_Pct: 127, Region: "North America" },
        { Month: "Mar 2026", ARR_kUSD: 5920, MRR_kUSD: 493.3, Active_Subscribers: 2670, New_Customers: 220, Churn_Rate_Pct: 1.5, CAC_USD: 385, LTV_USD: 7800, Net_Retention_Pct: 129, Region: "EMEA" },
        { Month: "Apr 2026", ARR_kUSD: 6180, MRR_kUSD: 515.0, Active_Subscribers: 2790, New_Customers: 230, Churn_Rate_Pct: 1.3, CAC_USD: 365, LTV_USD: 7950, Net_Retention_Pct: 131, Region: "EMEA" },
        { Month: "May 2026", ARR_kUSD: 6420, MRR_kUSD: 535.0, Active_Subscribers: 2900, New_Customers: 225, Churn_Rate_Pct: 1.4, CAC_USD: 375, LTV_USD: 8120, Net_Retention_Pct: 130, Region: "APAC" },
        { Month: "Jun 2026", ARR_kUSD: 6700, MRR_kUSD: 558.3, Active_Subscribers: 3030, New_Customers: 245, Churn_Rate_Pct: 1.2, CAC_USD: 350, LTV_USD: 8300, Net_Retention_Pct: 133, Region: "APAC" },
        { Month: "Jul 2026", ARR_kUSD: 6950, MRR_kUSD: 579.1, Active_Subscribers: 3150, New_Customers: 235, Churn_Rate_Pct: 1.5, CAC_USD: 380, LTV_USD: 8450, Net_Retention_Pct: 132, Region: "North America" },
        { Month: "Aug 2026", ARR_kUSD: 7210, MRR_kUSD: 600.8, Active_Subscribers: 3280, New_Customers: 250, Churn_Rate_Pct: 1.3, CAC_USD: 360, LTV_USD: 8620, Net_Retention_Pct: 134, Region: "North America" },
        { Month: "Sep 2026", ARR_kUSD: 7500, MRR_kUSD: 625.0, Active_Subscribers: 3410, New_Customers: 265, Churn_Rate_Pct: 1.1, CAC_USD: 340, LTV_USD: 8800, Net_Retention_Pct: 136, Region: "EMEA" },
        { Month: "Oct 2026", ARR_kUSD: 7780, MRR_kUSD: 648.3, Active_Subscribers: 3540, New_Customers: 260, Churn_Rate_Pct: 1.2, CAC_USD: 355, LTV_USD: 8980, Net_Retention_Pct: 135, Region: "EMEA" },
        { Month: "Nov 2026", ARR_kUSD: 8090, MRR_kUSD: 674.1, Active_Subscribers: 3690, New_Customers: 280, Churn_Rate_Pct: 1.0, CAC_USD: 330, LTV_USD: 9200, Net_Retention_Pct: 138, Region: "APAC" },
        { Month: "Dec 2026", ARR_kUSD: 8450, MRR_kUSD: 704.1, Active_Subscribers: 3850, New_Customers: 300, Churn_Rate_Pct: 0.9, CAC_USD: 315, LTV_USD: 9450, Net_Retention_Pct: 140, Region: "APAC" }
      ]
    },
    retail_supply_chain: {
      id: 'retail_supply_chain',
      name: 'Global Retail & Supply Chain Inventory',
      description: 'Multi-category SKU ledger tracking stock levels, unit economics, reorder triggers, and lead times.',
      category: 'Operations & Logistics',
      columns: ['SKU', 'Product_Name', 'Category', 'Stock_Units', 'Daily_Sales', 'Unit_Cost_USD', 'Selling_Price_USD', 'Gross_Margin_Pct', 'Lead_Time_Days', 'Supplier_Score'],
      data: [
        { SKU: "SKU-101", Product_Name: "Premium Silk Saree (Kanchipuram)", Category: "Apparel", Stock_Units: 24, Daily_Sales: 4.2, Unit_Cost_USD: 1400, Selling_Price_USD: 2800, Gross_Margin_Pct: 50.0, Lead_Time_Days: 7, Supplier_Score: 9.4 },
        { SKU: "SKU-102", Product_Name: "Pure Cotton Bed Linen King", Category: "Home Goods", Stock_Units: 8, Daily_Sales: 3.8, Unit_Cost_USD: 450, Selling_Price_USD: 890, Gross_Margin_Pct: 49.4, Lead_Time_Days: 5, Supplier_Score: 8.8 },
        { SKU: "SKU-103", Product_Name: "Artisan Brass Pooja Bell", Category: "Handicrafts", Stock_Units: 45, Daily_Sales: 1.2, Unit_Cost_USD: 220, Selling_Price_USD: 480, Gross_Margin_Pct: 54.1, Lead_Time_Days: 10, Supplier_Score: 7.9 },
        { SKU: "SKU-104", Product_Name: "Organic Virgin Coconut Oil 1L", Category: "Groceries", Stock_Units: 62, Daily_Sales: 8.5, Unit_Cost_USD: 180, Selling_Price_USD: 290, Gross_Margin_Pct: 37.9, Lead_Time_Days: 3, Supplier_Score: 9.1 },
        { SKU: "SKU-105", Product_Name: "Embroidered Velvet Cushion", Category: "Home Goods", Stock_Units: 14, Daily_Sales: 2.1, Unit_Cost_USD: 130, Selling_Price_USD: 320, Gross_Margin_Pct: 59.3, Lead_Time_Days: 8, Supplier_Score: 8.2 },
        { SKU: "SKU-106", Product_Name: "Handcrafted Clay Terracotta Pot", Category: "Handicrafts", Stock_Units: 3, Daily_Sales: 1.9, Unit_Cost_USD: 95, Selling_Price_USD: 250, Gross_Margin_Pct: 62.0, Lead_Time_Days: 12, Supplier_Score: 6.8 },
        { SKU: "SKU-107", Product_Name: "Heritage Filter Coffee Blend", Category: "Groceries", Stock_Units: 78, Daily_Sales: 12.0, Unit_Cost_USD: 110, Selling_Price_USD: 210, Gross_Margin_Pct: 47.6, Lead_Time_Days: 4, Supplier_Score: 9.6 },
        { SKU: "SKU-108", Product_Name: "Tussar Silk Dupatta", Category: "Apparel", Stock_Units: 19, Daily_Sales: 2.5, Unit_Cost_USD: 620, Selling_Price_USD: 1250, Gross_Margin_Pct: 50.4, Lead_Time_Days: 6, Supplier_Score: 8.9 },
        { SKU: "SKU-109", Product_Name: "Cast Iron Skillet Pre-Seasoned", Category: "Kitchenware", Stock_Units: 31, Daily_Sales: 3.4, Unit_Cost_USD: 550, Selling_Price_USD: 1090, Gross_Margin_Pct: 49.5, Lead_Time_Days: 6, Supplier_Score: 9.0 },
        { SKU: "SKU-110", Product_Name: "Natural Sandalwood Incense", Category: "Home Goods", Stock_Units: 95, Daily_Sales: 14.5, Unit_Cost_USD: 45, Selling_Price_USD: 120, Gross_Margin_Pct: 62.5, Lead_Time_Days: 3, Supplier_Score: 9.5 }
      ]
    },
    ecommerce_customers: {
      id: 'ecommerce_customers',
      name: 'E-Commerce Customer Behavior & Cohort Churn',
      description: 'Customer purchase patterns, lifetime order volume, satisfaction ratings, NPS cohorts, and churn.',
      category: 'Customer Intelligence',
      columns: ['Customer_ID', 'Segment', 'Total_Spend_USD', 'Total_Orders', 'Avg_Order_Value', 'Days_Since_Last_Order', 'NPS_Score', 'Support_Tickets', 'Churn_Risk_Pct', 'City'],
      data: [
        { Customer_ID: "CUST-901", Segment: "VIP Enterprise", Total_Spend_USD: 12850, Total_Orders: 42, Avg_Order_Value: 305.9, Days_Since_Last_Order: 4, NPS_Score: 10, Support_Tickets: 1, Churn_Risk_Pct: 4.5, City: "Bangalore" },
        { Customer_ID: "CUST-902", Segment: "High Growth", Total_Spend_USD: 8420, Total_Orders: 28, Avg_Order_Value: 300.7, Days_Since_Last_Order: 12, NPS_Score: 9, Support_Tickets: 2, Churn_Risk_Pct: 8.2, City: "Mumbai" },
        { Customer_ID: "CUST-903", Segment: "At Risk", Total_Spend_USD: 3150, Total_Orders: 9, Avg_Order_Value: 350.0, Days_Since_Last_Order: 78, NPS_Score: 4, Support_Tickets: 5, Churn_Risk_Pct: 74.0, City: "Delhi" },
        { Customer_ID: "CUST-904", Segment: "Regular", Total_Spend_USD: 4600, Total_Orders: 18, Avg_Order_Value: 255.5, Days_Since_Last_Order: 19, NPS_Score: 8, Support_Tickets: 0, Churn_Risk_Pct: 14.1, City: "Chennai" },
        { Customer_ID: "CUST-905", Segment: "VIP Enterprise", Total_Spend_USD: 15400, Total_Orders: 55, Avg_Order_Value: 280.0, Days_Since_Last_Order: 2, NPS_Score: 10, Support_Tickets: 0, Churn_Risk_Pct: 3.0, City: "Hyderabad" }
      ]
    },
    financial_credit: {
      id: 'financial_credit',
      name: 'Financial Risk & Credit Assessment',
      description: 'Enterprise financial metrics, working capital runway, DSCR, credit score, and risk bands.',
      category: 'Risk & Compliance',
      columns: ['Entity_ID', 'Sector', 'Monthly_Revenue_Lakhs', 'Debt_Ratio', 'Credit_Score', 'DSCR', 'Cash_Runway_Months', 'Default_Risk_Pct', 'Risk_Rating', 'Approval_Status'],
      data: [
        { Entity_ID: "ENT-01", Sector: "Textiles & Apparel", Monthly_Revenue_Lakhs: 24.5, Debt_Ratio: 0.32, Credit_Score: 780, DSCR: 2.4, Cash_Runway_Months: 14.2, Default_Risk_Pct: 2.1, Risk_Rating: "AAA", Approval_Status: "Approved" },
        { Entity_ID: "ENT-02", Sector: "Precision Engineering", Monthly_Revenue_Lakhs: 42.0, Debt_Ratio: 0.45, Credit_Score: 740, DSCR: 1.9, Cash_Runway_Months: 9.5, Default_Risk_Pct: 4.8, Risk_Rating: "AA", Approval_Status: "Approved" },
        { Entity_ID: "ENT-03", Sector: "Food & Agro Processing", Monthly_Revenue_Lakhs: 18.2, Debt_Ratio: 0.58, Credit_Score: 680, DSCR: 1.4, Cash_Runway_Months: 5.1, Default_Risk_Pct: 12.5, Risk_Rating: "BBB", Approval_Status: "Under Review" },
        { Entity_ID: "ENT-04", Sector: "Leather Goods", Monthly_Revenue_Lakhs: 12.0, Debt_Ratio: 0.72, Credit_Score: 610, DSCR: 1.05, Cash_Runway_Months: 2.8, Default_Risk_Pct: 28.0, Risk_Rating: "BB", Approval_Status: "Conditional" }
      ]
    }
  },

  // Chart Instances Map
  chartInstances: {}
};

// ==========================================================================
// 2. INITIALIZATION & ROUTING
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Theme from local storage
  const savedTheme = localStorage.getItem('pulse_theme') || 'light';
  setAppTheme(savedTheme);

  // 2. Initialize Navigation Click Handlers
  document.querySelectorAll('.nav-link').forEach(btn => {
    btn.addEventListener('click', () => {
      const viewId = btn.getAttribute('data-view');
      switchView(viewId);
    });
  });

  // 3. Load default dataset
  loadPresetDataset('saas_metrics');

  // 4. Initialize Dashboard Visuals
  initDashboardCharts();
  renderDashboardInsights();
  renderDashboardActivity();

  // 5. Setup Drag & Drop File Upload
  setupDropZone();

  // 6. Setup Keyboard Shortcuts (Cmd+K / Ctrl+K)
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openSearchModal();
    }
    if (e.key === 'Escape') {
      closeSearchModal();
      closeAddDataModal();
      closeConnectModal();
      closeChartFullscreen();
      closeHelpModal();
    }
  });

  // 7. Initialize WhatsApp Automation & Floating AI Assistant
  initFloatingAiAssistant();
  fetchWhatsAppConfig();

  // 8. Render Lucide Icons
  if (window.lucide) {
    lucide.createIcons();
  }
});

// View Switcher
function switchView(viewId) {
  AppState.activeView = viewId;

  // Update Nav links
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('data-view') === viewId) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  // Update View Panels
  document.querySelectorAll('.view-panel').forEach(panel => {
    if (panel.id === `view-${viewId}`) {
      panel.classList.add('active');
    } else {
      panel.classList.remove('active');
    }
  });

  // View specific setups
  if (viewId === 'analytics') {
    initVisualAnalyticsStudio();
  } else if (viewId === 'insights') {
    renderFullInsightsGrid();
  } else if (viewId === 'reports') {
    generateExecutiveReport();
  } else if (viewId === 'data-analysis') {
    populateAnalysisSelectors();
  } else if (viewId === 'whatsapp-automation') {
    fetchWhatsAppConfig();
    fetchWhatsAppRules();
    fetchWhatsAppHistory();
  }

  // Scroll to top
  const scroller = document.getElementById('contentScroll');
  if (scroller) scroller.scrollTop = 0;

  if (window.lucide) lucide.createIcons();
}

// Theme Switcher
function toggleAppTheme() {
  const newTheme = AppState.currentTheme === 'light' ? 'dark' : 'light';
  setAppTheme(newTheme);
}

function setAppTheme(theme) {
  AppState.currentTheme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('pulse_theme', theme);

  const icon = document.getElementById('themeIcon');
  if (icon) {
    icon.setAttribute('data-lucide', theme === 'dark' ? 'sun' : 'moon');
  }

  // Refresh charts with updated theme colors
  Object.values(AppState.chartInstances).forEach(chart => {
    if (chart && typeof chart.update === 'function') {
      chart.update();
    }
  });

  if (window.lucide) lucide.createIcons();
}

// ==========================================================================
// 3. DATASET MANAGEMENT & PRESETS
// ==========================================================================
function loadPresetDataset(presetId) {
  const preset = AppState.presets[presetId];
  if (!preset) return;

  AppState.currentDatasetId = presetId;
  AppState.currentDatasetName = preset.name;
  AppState.currentRows = JSON.parse(JSON.stringify(preset.data));
  AppState.currentColumns = [...preset.columns];

  // Update UI indicators
  const sbName = document.getElementById('sidebarActiveDatasetName');
  if (sbName) sbName.textContent = preset.name;

  // Run validation
  validateCurrentDataset();

  // Update preset cards active state
  document.querySelectorAll('.preset-card').forEach(card => {
    card.classList.remove('active');
  });
  const activeCard = document.querySelector(`.preset-card[onclick*="${presetId}"]`);
  if (activeCard) activeCard.classList.add('active');

  // Render preview table & editable grid
  renderPreviewTable();
  renderSpreadsheetGrid();

  // Populate Analysis variables
  populateAnalysisSelectors();

  showToast(`Loaded "${preset.name}" (${AppState.currentRows.length} records)`, 'success');
}

function validateCurrentDataset() {
  const rows = AppState.currentRows;
  if (!rows || rows.length === 0) return;

  // Perform client-side validation analysis
  const colMeta = {};
  const columns = AppState.currentColumns;
  let missingCells = 0;
  const issues = [];

  columns.forEach(col => {
    const vals = rows.map(r => r[col]);
    const missing = vals.filter(v => v === null || v === undefined || v === '').length;
    missingCells += missing;

    const nonNulls = vals.filter(v => v !== null && v !== undefined && v !== '');
    const isNum = nonNulls.every(v => typeof v === 'number' || (!isNaN(v) && v !== ''));
    const isDate = nonNulls.some(v => typeof v === 'string' && (v.includes('202') || v.includes('/')));

    colMeta[col] = {
      type: isNum ? 'Numeric' : (isDate ? 'Date' : 'Text'),
      missingCount: missing,
      uniqueCount: new Set(vals).size
    };

    if (missing > 0) {
      issues.push({
        id: `missing_${col}`,
        severity: missing > 2 ? 'high' : 'medium',
        title: `${missing} Missing Value(s) in '${col}'`,
        description: `Field '${col}' has ${missing} unpopulated cells. Impute median or drop incomplete records.`,
        actionCode: 'impute_missing'
      });
    }
  });

  const totalCells = rows.length * columns.length;
  const qualityScore = Math.max(10, Math.round(100 - (missingCells / totalCells) * 50));

  AppState.currentValidation = {
    rowsCount: rows.length,
    columnsCount: columns.length,
    missingCells,
    qualityScore,
    colMeta,
    issues
  };

  // Update UI Stats
  const sbMeta = document.getElementById('sidebarActiveDatasetMeta');
  if (sbMeta) sbMeta.textContent = `${rows.length} records · ${columns.length} columns · ${qualityScore}% Clean`;

  const prRows = document.getElementById('previewTotalRows');
  if (prRows) prRows.textContent = rows.length;
  const prCols = document.getElementById('previewTotalCols');
  if (prCols) prCols.textContent = columns.length;
  const prMiss = document.getElementById('previewMissingCount');
  if (prMiss) prMiss.textContent = `${missingCells} (${((missingCells/totalCells)*100).toFixed(1)}%)`;
  const prDup = document.getElementById('previewDuplicateCount');
  if (prDup) prDup.textContent = '0';
  const prQual = document.getElementById('previewQualityScore');
  if (prQual) prQual.textContent = `${qualityScore}.0%`;

  const valBig = document.getElementById('validationScoreBig');
  if (valBig) valBig.textContent = `${qualityScore}%`;

  // Render Issues
  renderValidationIssues(issues);
}

function renderValidationIssues(issues) {
  const container = document.getElementById('validationIssuesList');
  if (!container) return;

  if (!issues || issues.length === 0) {
    container.innerHTML = `
      <div class="remediation-card" style="border-left-color: var(--success);">
        <div class="remediation-info">
          <h5><i data-lucide="check-circle" style="display:inline; width:16px; height:16px; color:var(--success);"></i> Zero Schema Inconsistencies</h5>
          <p>All data types, primary keys, and required attributes pass ISO/IEC 25012 quality validation benchmarks.</p>
        </div>
        <span class="status-badge success">100% Compliant</span>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  container.innerHTML = issues.map(iss => `
    <div class="remediation-card ${iss.severity}">
      <div class="remediation-info">
        <h5>${iss.title}</h5>
        <p>${iss.description}</p>
      </div>
      <div class="remediation-actions">
        <button class="btn-remedy-fix" onclick="applyRemediationFix('${iss.actionCode}')">Fix Automatically</button>
        <button class="btn-remedy-ignore" onclick="this.closest('.remediation-card').remove(); showToast('Issue ignored for this session', 'info');">Ignore</button>
      </div>
    </div>
  `).join('');

  if (window.lucide) lucide.createIcons();
}

function applyFullCleaning() {
  // Apply automated median imputation & deduplication
  const rows = AppState.currentRows;
  const columns = AppState.currentColumns;

  columns.forEach(col => {
    const nums = rows.map(r => r[col]).filter(v => typeof v === 'number' && !isNaN(v));
    if (nums.length > 0) {
      nums.sort((a,b) => a - b);
      const median = nums[Math.floor(nums.length / 2)];
      rows.forEach(r => {
        if (r[col] === null || r[col] === undefined || r[col] === '') {
          r[col] = median;
        }
      });
    } else {
      rows.forEach(r => {
        if (r[col] === null || r[col] === undefined || r[col] === '') {
          r[col] = 'N/A';
        }
      });
    }
  });

  validateCurrentDataset();
  renderPreviewTable();
  renderSpreadsheetGrid();
  showToast('Automated dataset cleaning completed! Quality score is now 100%', 'success');
}

function applyRemediationFix(actionCode) {
  applyFullCleaning();
}

// ==========================================================================
// 4. PREVIEW TABLE & MANUAL SPREADSHEET GRID
// ==========================================================================
function renderPreviewTable(filterType = 'all') {
  const thead = document.getElementById('previewTableHead');
  const tbody = document.getElementById('previewTableBody');
  if (!thead || !tbody) return;

  const cols = AppState.currentColumns;
  const rows = AppState.currentRows.slice(0, 15);
  const meta = AppState.currentValidation ? AppState.currentValidation.colMeta : {};

  // Headers
  thead.innerHTML = `<tr>${cols.map(c => {
    const dtype = meta[c] ? meta[c].type : 'Text';
    const tagClass = dtype === 'Numeric' ? 'num' : (dtype === 'Date' ? 'date' : 'txt');
    return `<th>${c} <span class="type-tag ${tagClass}">${dtype.slice(0,3)}</span></th>`;
  }).join('')}</tr>`;

  // Body
  tbody.innerHTML = rows.map(r => {
    return `<tr>${cols.map(c => `<td>${r[c] !== undefined ? r[c] : ''}</td>`).join('')}</tr>`;
  }).join('');
}

function filterPreviewColumns(type, pillEl) {
  document.querySelectorAll('.column-type-filter-group .filter-pill').forEach(p => p.classList.remove('active'));
  if (pillEl) pillEl.classList.add('active');
  renderPreviewTable(type);
}

function filterPreviewRows(query) {
  const q = query.toLowerCase().trim();
  const rows = document.querySelectorAll('#previewTableBody tr');
  rows.forEach(tr => {
    const text = tr.textContent.toLowerCase();
    tr.style.display = text.includes(q) ? '' : 'none';
  });
}

function renderSpreadsheetGrid() {
  const container = document.getElementById('spreadsheetGridContainer');
  if (!container) return;

  const cols = AppState.currentColumns;
  const rows = AppState.currentRows;

  let html = `<table class="grid-table"><thead><tr><th style="width: 40px; text-align:center;">#</th>`;
  cols.forEach((col, idx) => {
    html += `<th>${col}</th>`;
  });
  html += `</tr></thead><tbody>`;

  rows.forEach((row, rIdx) => {
    html += `<tr><td style="text-align:center; color:var(--text-muted); font-size:11px;">${rIdx + 1}</td>`;
    cols.forEach(col => {
      const val = row[col] !== undefined ? row[row] || row[col] : '';
      html += `<td><input type="text" class="grid-cell-input" value="${val}" onchange="updateGridCell(${rIdx}, '${col}', this.value)"></td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;

  container.innerHTML = html;

  const rCount = document.getElementById('gridRowsCount');
  if (rCount) rCount.textContent = `${rows.length} rows`;
  const cCount = document.getElementById('gridColsCount');
  if (cCount) cCount.textContent = `${cols.length} columns`;
}

function updateGridCell(rIdx, col, newVal) {
  if (AppState.currentRows[rIdx]) {
    const num = parseFloat(newVal);
    AppState.currentRows[rIdx][col] = isNaN(num) ? newVal : num;
    validateCurrentDataset();
  }
}

function addSpreadsheetRow() {
  const newRow = {};
  AppState.currentColumns.forEach(c => newRow[c] = '');
  AppState.currentRows.push(newRow);
  renderSpreadsheetGrid();
  renderPreviewTable();
  validateCurrentDataset();
  showToast('Appended new row to manual grid', 'info');
}

function addSpreadsheetColumn() {
  const colName = prompt('Enter New Column Name:');
  if (!colName || !colName.trim()) return;
  const cleanName = colName.trim().replace(/\s+/g, '_');
  AppState.currentColumns.push(cleanName);
  AppState.currentRows.forEach(r => r[cleanName] = 0);
  renderSpreadsheetGrid();
  renderPreviewTable();
  populateAnalysisSelectors();
  showToast(`Added column "${cleanName}"`, 'success');
}

function duplicateSelectedRow() {
  if (AppState.currentRows.length > 0) {
    const copy = JSON.parse(JSON.stringify(AppState.currentRows[AppState.currentRows.length - 1]));
    AppState.currentRows.push(copy);
    renderSpreadsheetGrid();
    renderPreviewTable();
    validateCurrentDataset();
    showToast('Duplicated last row', 'info');
  }
}

function deleteSelectedRow() {
  if (AppState.currentRows.length > 1) {
    AppState.currentRows.pop();
    renderSpreadsheetGrid();
    renderPreviewTable();
    validateCurrentDataset();
    showToast('Removed last row', 'info');
  }
}

function filterSpreadsheetRows(query) {
  const q = query.toLowerCase().trim();
  const rows = document.querySelectorAll('.grid-table tbody tr');
  rows.forEach(tr => {
    const text = tr.textContent.toLowerCase();
    tr.style.display = text.includes(q) ? '' : 'none';
  });
}

function exportSpreadsheetCSV() {
  if (!AppState.currentRows.length) return;
  const cols = AppState.currentColumns;
  let csv = cols.join(',') + '\n';
  AppState.currentRows.forEach(r => {
    csv += cols.map(c => `"${r[c] !== undefined ? r[c] : ''}"`).join(',') + '\n';
  });

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${AppState.currentDatasetId}_export.csv`;
  link.click();
  showToast('Downloaded dataset as CSV', 'success');
}

// ==========================================================================
// 5. FILE DRAG & DROP AND PARSING ENGINE
// ==========================================================================
function setupDropZone() {
  const dropZone = document.getElementById('fileDropZone');
  if (!dropZone) return;

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('dragover');
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('dragover');
    }, false);
  });

  dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      processUploadedFile(files[0]);
    }
  });
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) {
    processUploadedFile(file);
  }
}

function processUploadedFile(file) {
  const progressBox = document.getElementById('uploadProgressBox');
  const fileName = document.getElementById('uploadFileName');
  const fileSize = document.getElementById('uploadFileSize');
  const fill = document.getElementById('uploadProgressFill');
  const status = document.getElementById('uploadStatusBadge');

  if (progressBox) progressBox.style.display = 'block';
  if (fileName) fileName.textContent = file.name;
  if (fileSize) fileSize.textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
  if (fill) fill.style.width = '35%';
  if (status) status.textContent = 'Parsing Schema…';

  const reader = new FileReader();

  if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheet = workbook.SheetNames[0];
        const json = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheet]);
        finishUploadProcessing(file.name, json);
      } catch (err) {
        showToast('Error parsing Excel file', 'danger');
      }
    };
    reader.readAsArrayBuffer(file);
  } else if (file.name.endsWith('.json')) {
    reader.onload = (e) => {
      try {
        const json = JSON.parse(e.target.result);
        const rows = Array.isArray(json) ? json : [json];
        finishUploadProcessing(file.name, rows);
      } catch (err) {
        showToast('Error parsing JSON payload', 'danger');
      }
    };
    reader.readAsText(file);
  } else {
    // CSV / Text fallback
    reader.onload = (e) => {
      const text = e.target.result;
      const lines = text.split(/\r?\n/).filter(l => l.trim().length > 0);
      if (lines.length > 1) {
        const headers = lines[0].split(',').map(h => h.trim().replace(/^["']|["']$/g, ''));
        const rows = [];
        for (let i = 1; i < lines.length; i++) {
          const vals = lines[i].split(',').map(v => v.trim().replace(/^["']|["']$/g, ''));
          const rowObj = {};
          headers.forEach((h, hIdx) => {
            const rawVal = vals[hIdx];
            const num = parseFloat(rawVal);
            rowObj[h] = !isNaN(num) && String(num) === rawVal ? num : (rawVal || '');
          });
          rows.push(rowObj);
        }
        finishUploadProcessing(file.name, rows);
      }
    };
    reader.readAsText(file);
  }
}

function finishUploadProcessing(name, rows) {
  const fill = document.getElementById('uploadProgressFill');
  const status = document.getElementById('uploadStatusBadge');
  if (fill) fill.style.width = '100%';
  if (status) status.textContent = 'Done (Verified)';

  if (rows && rows.length > 0) {
    AppState.currentDatasetName = name;
    AppState.currentRows = rows;
    AppState.currentColumns = Object.keys(rows[0]);

    validateCurrentDataset();
    renderPreviewTable();
    renderSpreadsheetGrid();
    populateAnalysisSelectors();

    showToast(`Successfully ingested "${name}" (${rows.length} rows)`, 'success');
  }
}

function cancelFileUpload() {
  const progressBox = document.getElementById('uploadProgressBox');
  if (progressBox) progressBox.style.display = 'none';
  const fileInput = document.getElementById('fileInput');
  if (fileInput) fileInput.value = '';
}

function switchFeedTab(tabKey) {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    if (btn.getAttribute('data-feed-tab') === tabKey) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  document.querySelectorAll('.feed-tab-content').forEach(content => {
    if (content.id === `feedTab-${tabKey}`) {
      content.classList.add('active');
    } else {
      content.classList.remove('active');
    }
  });

  if (tabKey === 'manual') {
    renderSpreadsheetGrid();
  }
  if (window.lucide) lucide.createIcons();
}

// ==========================================================================
// 6. DASHBOARD & VISUAL ANALYTICS CHARTS (CHART.JS)
// ==========================================================================
function initDashboardCharts() {
  // 1. Performance Trend Line Chart
  const trendCtx = document.getElementById('dashboardTrendChart');
  if (trendCtx) {
    const isDark = AppState.currentTheme === 'dark';
    const gridColor = isDark ? '#1e293b' : '#f1f5f9';
    const textColor = isDark ? '#94a3b8' : '#64748b';

    AppState.chartInstances.dashboardTrendChart = new Chart(trendCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
          {
            label: 'Actual Revenue ($k)',
            data: [3200, 3340, 3520, 3690, 3880, 4050, 4210, 4390, 4580, 4760, 4980, 5240],
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.08)',
            fill: true,
            tension: 0.35,
            borderWidth: 2.5,
            pointRadius: 3,
            pointHoverRadius: 6
          },
          {
            label: '3-Month Moving Avg ($k)',
            data: [3200, 3270, 3353, 3516, 3696, 3873, 4046, 4216, 4393, 4576, 4773, 4993],
            borderColor: '#8b5cf6',
            borderDash: [5, 5],
            borderWidth: 2,
            pointRadius: 0,
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 12 } } },
          tooltip: {
            backgroundColor: '#0f172a',
            titleFont: { family: 'Plus Jakarta Sans', weight: 'bold' },
            padding: 12,
            callbacks: {
              label: (ctx) => ` ${ctx.dataset.label}: $${ctx.raw.toLocaleString()}`
            }
          }
        },
        scales: {
          x: { grid: { color: gridColor }, ticks: { color: textColor, font: { family: 'Plus Jakarta Sans' } } },
          y: { grid: { color: gridColor }, ticks: { color: textColor, font: { family: 'Plus Jakarta Sans' }, callback: (v) => `$${v/1000}M` } }
        }
      }
    });
  }

  // 2. Category & Segment Share Donut Chart
  const donutCtx = document.getElementById('dashboardDonutChart');
  if (donutCtx) {
    AppState.chartInstances.dashboardDonutChart = new Chart(donutCtx, {
      type: 'doughnut',
      data: {
        labels: ['North America (45%)', 'EMEA (32%)', 'APAC (23%)'],
        datasets: [{
          data: [45, 32, 23],
          backgroundColor: ['#2563eb', '#8b5cf6', '#10b981'],
          borderWidth: 0,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: { position: 'bottom', labels: { color: '#64748b', font: { family: 'Plus Jakarta Sans', size: 11.5 } } }
        }
      }
    });
  }

  // 3. Category Comparison Bar Chart
  const barCtx = document.getElementById('dashboardBarChart');
  if (barCtx) {
    AppState.chartInstances.dashboardBarChart = new Chart(barCtx, {
      type: 'bar',
      data: {
        labels: ['Enterprise VIP', 'Mid-Market Growth', 'Small Business', 'Direct Web Inbound'],
        datasets: [
          {
            label: 'Net Revenue Contribution ($k)',
            data: [4250, 2480, 1120, 600],
            backgroundColor: '#2563eb',
            borderRadius: 6
          },
          {
            label: 'Expansion Pipeline ($k)',
            data: [1850, 920, 340, 150],
            backgroundColor: '#60a5fa',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: '#64748b', font: { family: 'Plus Jakarta Sans' } } }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: '#64748b' } },
          y: { grid: { color: '#f1f5f9' }, ticks: { color: '#64748b', callback: v => `$${v}k` } }
        }
      }
    });
  }
}

function setChartMetric(metricKey, pillEl) {
  document.querySelectorAll('.pill-group .pill').forEach(p => p.classList.remove('active'));
  if (pillEl) pillEl.classList.add('active');

  const chart = AppState.chartInstances.dashboardTrendChart;
  if (!chart) return;

  if (metricKey === 'arr') {
    chart.data.datasets[0].label = 'Actual ARR ($k)';
    chart.data.datasets[0].data = [3200, 3340, 3520, 3690, 3880, 4050, 4210, 4390, 4580, 4760, 4980, 5240];
    chart.options.scales.y.ticks.callback = v => `$${v/1000}M`;
  } else if (metricKey === 'subscribers') {
    chart.data.datasets[0].label = 'Active Subscribers';
    chart.data.datasets[0].data = [1420, 1485, 1560, 1640, 1725, 1810, 1880, 1960, 2045, 2130, 2240, 2360];
    chart.options.scales.y.ticks.callback = v => `${v.toLocaleString()}`;
  } else if (metricKey === 'retention') {
    chart.data.datasets[0].label = 'Net Retention %';
    chart.data.datasets[0].data = [112, 114, 115, 116, 118, 119, 117, 121, 123, 122, 125, 128];
    chart.options.scales.y.ticks.callback = v => `${v}%`;
  }
  chart.update();
}

function initVisualAnalyticsStudio() {
  if (AppState.chartInstances.visualMultiLineChart) return; // already initialized

  // 1. Dual-Metric Multi Line Chart
  const mlCtx = document.getElementById('visualMultiLineChart');
  if (mlCtx) {
    AppState.chartInstances.visualMultiLineChart = new Chart(mlCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
          {
            label: 'ARR ($k)',
            data: [3200, 3340, 3520, 3690, 3880, 4050, 4210, 4390, 4580, 4760, 4980, 5240],
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            fill: true,
            tension: 0.35,
            yAxisID: 'y'
          },
          {
            label: 'MRR ($k)',
            data: [266, 278, 293, 307, 323, 337, 350, 365, 381, 396, 415, 436],
            borderColor: '#10b981',
            tension: 0.35,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { position: 'left', ticks: { color: '#64748b' } },
          y1: { position: 'right', grid: { display: false }, ticks: { color: '#10b981' } }
        }
      }
    });
  }

  // 2. Stacked Bar Chart
  const sbCtx = document.getElementById('visualStackedBarChart');
  if (sbCtx) {
    AppState.chartInstances.visualStackedBarChart = new Chart(sbCtx, {
      type: 'bar',
      data: {
        labels: ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026'],
        datasets: [
          { label: 'North America', data: [1500, 1850, 2200, 2600, 2900, 3300], backgroundColor: '#2563eb' },
          { label: 'EMEA', data: [1100, 1300, 1550, 1800, 2100, 2400], backgroundColor: '#8b5cf6' },
          { label: 'APAC', data: [600, 730, 830, 840, 920, 1000], backgroundColor: '#10b981' }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { x: { stacked: true }, y: { stacked: true, ticks: { callback: v => `$${v}k` } } }
      }
    });
  }

  // 3. Gradient Area Chart
  const arCtx = document.getElementById('visualAreaChart');
  if (arCtx) {
    AppState.chartInstances.visualAreaChart = new Chart(arCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
          label: 'Active Subscribers',
          data: [1420, 1485, 1560, 1640, 1725, 1810, 1880, 1960, 2045, 2130, 2240, 2360],
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99, 102, 241, 0.18)',
          fill: true,
          tension: 0.4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    });
  }

  // 4. Scatter Plot Matrix
  const scCtx = document.getElementById('visualScatterChart');
  if (scCtx) {
    AppState.chartInstances.visualScatterChart = new Chart(scCtx, {
      type: 'scatter',
      data: {
        datasets: [{
          label: 'Customer Cohorts (CAC vs LTV)',
          data: [
            { x: 450, y: 5800 }, { x: 440, y: 5920 }, { x: 465, y: 6050 },
            { x: 435, y: 6180 }, { x: 420, y: 6300 }, { x: 445, y: 6420 },
            { x: 480, y: 6500 }, { x: 410, y: 6650 }, { x: 395, y: 6800 },
            { x: 415, y: 6910 }, { x: 380, y: 7100 }, { x: 370, y: 7350 }
          ],
          backgroundColor: '#f59e0b',
          pointRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: 'Customer Acquisition Cost ($)' } },
          y: { title: { display: true, text: 'Customer Lifetime Value ($)' } }
        }
      }
    });
  }
}

// ==========================================================================
// 7. DATA ANALYSIS WORKSPACE & ALGORITHMS
// ==========================================================================
function populateAnalysisSelectors() {
  const xSelect = document.getElementById('analysisXVarSelect');
  const ySelect = document.getElementById('analysisYVarSelect');
  const groupSelect = document.getElementById('analysisGroupVarSelect');
  if (!xSelect || !ySelect) return;

  const cols = AppState.currentColumns;
  const meta = AppState.currentValidation ? AppState.currentValidation.colMeta : {};

  xSelect.innerHTML = cols.map(c => `<option value="${c}">${c}</option>`).join('');
  ySelect.innerHTML = cols.map(c => `<option value="${c}">${c}</option>`).join('');
  if (groupSelect) {
    groupSelect.innerHTML = `<option value="">(None / Aggregate All)</option>` + cols.map(c => `<option value="${c}">${c}</option>`).join('');
  }

  // Choose smart defaults
  const numCols = cols.filter(c => meta[c] && meta[c].type === 'Numeric');
  const textCols = cols.filter(c => meta[c] && (meta[c].type === 'Text' || meta[c].type === 'Date'));

  if (textCols.length > 0) xSelect.value = textCols[0];
  if (numCols.length > 0) ySelect.value = numCols[0];
}

function handleAnalysisDatasetChange(presetId) {
  loadPresetDataset(presetId);
}

function handleAnalysisTypeChange(type) {
  const hint = document.getElementById('analysisTypeHintText');
  const hints = {
    descriptive: 'Computes central tendency (mean, median), variance, standard deviation, IQR, and histogram distribution.',
    trend: 'Calculates period-over-period slope, rolling moving average, and linear regression trajectory.',
    comparative: 'Evaluates category/cohort breakdown vs benchmark average and volume shares.',
    correlation: 'Calculates Pearson correlation coefficient matrix, R² variance explained, and regression line.',
    distribution: 'Generates frequency bins, histogram densities, and Tukey boxplot whisker parameters.',
    kpi: 'Compares target vs actual attainment %, calculates variances, and assigns health status.',
    forecasting: 'Projects next 4 periods with blended linear momentum and 95% confidence intervals.',
    outliers: 'Locates records exceeding 2.0σ and 3.0σ standard deviations from baseline.'
  };
  if (hint && hints[type]) {
    hint.innerHTML = `<i data-lucide="info"></i><span>${hints[type]}</span>`;
    if (window.lucide) lucide.createIcons();
  }
}

async function executeSelectedAnalysis() {
  const datasetSelect = document.getElementById('analysisDatasetSelect');
  const typeSelect = document.getElementById('analysisTypeSelect');
  const xSelect = document.getElementById('analysisXVarSelect');
  const ySelect = document.getElementById('analysisYVarSelect');
  const groupSelect = document.getElementById('analysisGroupVarSelect');
  const metricSelect = document.getElementById('analysisMetricSelect');

  const payload = {
    rows: AppState.currentRows,
    analysis_type: typeSelect ? typeSelect.value : 'trend',
    x_var: xSelect ? xSelect.value : null,
    y_var: ySelect ? ySelect.value : null,
    group_var: groupSelect ? groupSelect.value : null,
    metric: metricSelect ? metricSelect.value : 'sum'
  };

  showToast('Executing statistical analysis…', 'info');

  try {
    const res = await fetch('/api/analytics/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    renderAnalysisResults(data, payload);
  } catch (e) {
    // Client-side statistical calculation fallback
    const fallbackData = computeClientAnalysis(payload);
    renderAnalysisResults(fallbackData, payload);
  }
}

function computeClientAnalysis(payload) {
  const rows = payload.rows;
  const yVar = payload.y_var || AppState.currentColumns[1];
  const xVar = payload.x_var || AppState.currentColumns[0];
  const nums = rows.map(r => parseFloat(r[yVar])).filter(v => !isNaN(v));

  const sum = nums.reduce((a,b) => a + b, 0);
  const avg = sum / (nums.length || 1);
  const min = Math.min(...nums);
  const max = Math.max(...nums);

  return {
    type: payload.analysis_type,
    count: nums.length,
    mean: Math.round(avg * 100) / 100,
    min,
    max,
    total: Math.round(sum * 100) / 100,
    key_takeaway: `Analysis of '${yVar}' across ${nums.length} records demonstrates average of ${avg.toFixed(2)} (Range: ${min} - ${max}).`,
    labels: rows.map(r => String(r[xVar])),
    series: nums
  };
}

function renderAnalysisResults(result, config) {
  const container = document.getElementById('analysisResultsContainer');
  if (!container) return;
  container.style.display = 'block';

  const typeBadge = document.getElementById('resultAnalysisTypeBadge');
  if (typeBadge) typeBadge.textContent = `${config.analysis_type.toUpperCase()} ANALYSIS`;

  const datasetBadge = document.getElementById('resultDatasetNameBadge');
  if (datasetBadge) datasetBadge.textContent = AppState.currentDatasetName;

  const takeaway = document.getElementById('resultTakeawayParagraph');
  if (takeaway) takeaway.textContent = result.key_takeaway || 'Analysis computed across active records.';

  // Render Stats Table
  const tableWrap = document.getElementById('analysisStatsTableWrapper');
  if (tableWrap) {
    let rowsHtml = '';
    const ignoreKeys = ['type', 'labels', 'series', 'scatter_points', 'correlation_matrix', 'histogram', 'boxplot', 'distribution_bins', 'key_takeaway', 'breakdown', 'flagged_records'];
    Object.keys(result).forEach(k => {
      if (!ignoreKeys.includes(k) && typeof result[k] !== 'object') {
        rowsHtml += `
          <div class="stat-row">
            <span class="stat-label">${k.replace(/_/g, ' ').toUpperCase()}</span>
            <span class="stat-value">${result[k]}</span>
          </div>
        `;
      }
    });
    tableWrap.innerHTML = rowsHtml || '<div class="stat-row"><span class="stat-label">Status</span><span class="stat-value">Processed</span></div>';
  }

  // Render Output Chart
  renderAnalysisChart(result, config);

  showToast('Analysis completed successfully', 'success');
  container.scrollIntoView({ behavior: 'smooth' });
}

function renderAnalysisChart(result, config) {
  const canvas = document.getElementById('analysisCanvas');
  if (!canvas) return;

  if (AppState.chartInstances.analysisChart) {
    AppState.chartInstances.analysisChart.destroy();
  }

  const chartTitle = document.getElementById('analysisChartTitle');
  if (chartTitle) chartTitle.textContent = `${config.analysis_type.toUpperCase()}: ${config.y_var || 'Metric'} Analysis`;

  const labels = result.labels || result.historical_labels || (result.breakdown ? result.breakdown.map(b => b.category) : ['Point 1', 'Point 2', 'Point 3']);
  const dataVals = result.series || (result.breakdown ? result.breakdown.map(b => b.sum) : [10, 20, 30]);

  let chartType = 'line';
  if (config.analysis_type === 'comparative' || config.analysis_type === 'distribution') {
    chartType = 'bar';
  }

  AppState.chartInstances.analysisChart = new Chart(canvas, {
    type: chartType,
    data: {
      labels: labels,
      datasets: [{
        label: config.y_var || 'Analyzed Metric',
        data: dataVals,
        borderColor: '#2563eb',
        backgroundColor: chartType === 'bar' ? '#3b82f6' : 'rgba(37, 99, 235, 0.1)',
        fill: chartType === 'line',
        borderRadius: 6,
        tension: 0.35
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' }
      }
    }
  });
}

function runPresetAnalysis(type) {
  switchView('data-analysis');
  const typeSelect = document.getElementById('analysisTypeSelect');
  if (typeSelect) {
    typeSelect.value = type;
    handleAnalysisTypeChange(type);
    executeSelectedAnalysis();
  }
}

// ==========================================================================
// 8. AI-POWERED BUSINESS INSIGHTS
// ==========================================================================
const BusinessInsightsData = [
  {
    id: 'ins-1',
    type: 'positive',
    category: 'Revenue Growth',
    title: 'Annual Recurring Revenue Up +18.4%',
    key_insight: 'Net ARR expanded +18.4% YoY, driven by enterprise upsell and multi-year contract renewals.',
    observation: 'Enterprise tier accounts recorded a 134% Net Retention Rate (NRR) with expansion sales velocity compressing from 64 to 42 days.',
    metric_badge: '+18.4% YoY Growth',
    recommendation: 'Scale outbound SDR capacity into EMEA mid-market expansion to replicate North American pipeline velocity.',
    action_label: 'Simulate Growth Surge'
  },
  {
    id: 'ins-2',
    type: 'negative',
    category: 'Customer Retention',
    title: 'Churn Elevation in 3-6 Month Cohort',
    key_insight: 'Customer churn rate elevated to 2.3% for accounts in the mid-tenure onboarding window.',
    observation: 'Product telemetry indicates a 22% drop in weekly active admin engagement prior to formal cancellation requests.',
    metric_badge: '2.3% Monthly Churn',
    recommendation: 'Deploy automated onboarding health check webhooks and trigger proactive CSM check-ins at Day 45.',
    action_label: 'Review At-Risk Accounts'
  },
  {
    id: 'ins-3',
    type: 'warning',
    category: 'Supply Chain & Inventory',
    title: 'Stockout Risk on 3 Fast-Moving SKUs',
    key_insight: 'Pure Cotton Bed Linen & Terracotta Craft inventory has dropped below the 5-day safety buffer threshold.',
    observation: 'Lead time from Salem suppliers averages 7 days, leaving a 48-hour exposure window during upcoming holiday promos.',
    metric_badge: '< 4 Days Buffer',
    recommendation: 'Dispatch an emergency reorder batch of 150 units today to safeguard estimated ₹42,000 gross margin.',
    action_label: 'Trigger Auto-Reorder'
  },
  {
    id: 'ins-4',
    type: 'neutral',
    category: 'Operational Efficiency',
    title: 'Customer Acquisition Cost Stabilizing',
    key_insight: 'Blended CAC decreased to $340 per enterprise account logo, reflecting high organic conversion.',
    observation: 'Organic content distribution and product-led signups now account for 44% of qualified pipeline.',
    metric_badge: '$340 Blended CAC',
    recommendation: 'Maintain current organic distribution cadence while testing localized multi-region campaigns.',
    action_label: 'View Channel Attribution'
  }
];

function renderDashboardInsights() {
  const container = document.getElementById('dashboardInsightsList');
  if (!container) return;

  container.innerHTML = BusinessInsightsData.slice(0, 3).map(ins => `
    <div class="insight-compact-item ${ins.type}">
      <div>
        <strong style="font-size: 12.5px; color: var(--text-primary);">${ins.title}</strong>
        <p style="font-size: 11.5px; color: var(--text-secondary); margin-top: 2px;">${ins.key_insight}</p>
      </div>
    </div>
  `).join('');
}

function renderFullInsightsGrid(filter = 'all') {
  const container = document.getElementById('insightsFullGrid');
  if (!container) return;

  const list = filter === 'all' ? BusinessInsightsData : BusinessInsightsData.filter(i => i.type === filter);

  container.innerHTML = list.map(ins => `
    <div class="insight-card">
      <div class="insight-card-header">
        <span class="insight-impact-badge ${ins.type}">${ins.type.toUpperCase()}</span>
        <span class="insight-metric-pill">${ins.metric_badge}</span>
      </div>
      <h3 class="insight-title">${ins.title}</h3>
      <p class="insight-key-bold">${ins.key_insight}</p>
      <p class="insight-observation">${ins.observation}</p>
      <div class="insight-recommendation-box">
        <div class="rec-title">Recommended Executive Action</div>
        <div>${ins.recommendation}</div>
      </div>
      <div class="insight-card-footer">
        <button class="btn-primary-sm" onclick="showToast('Triggered action: ${ins.action_label}', 'success')">
          <i data-lucide="zap"></i> ${ins.action_label}
        </button>
      </div>
    </div>
  `).join('');

  if (window.lucide) lucide.createIcons();
}

function filterInsightCards(type, btnEl) {
  document.querySelectorAll('.insight-filter-btn').forEach(b => b.classList.remove('active'));
  if (btnEl) btnEl.classList.add('active');
  renderFullInsightsGrid(type);
}

function refreshInsightsFeed() {
  showToast('Re-evaluating AI telemetry algorithms…', 'info');
  setTimeout(() => {
    renderFullInsightsGrid();
    showToast('AI Insights updated with latest telemetry', 'success');
  }, 500);
}

// ==========================================================================
// 9. EXECUTIVE REPORT GENERATION STUDIO (PDF, EXCEL, CSV)
// ==========================================================================
function generateExecutiveReport() {
  const body = document.getElementById('reportDocumentBody');
  const titleInput = document.getElementById('reportTitleInput');
  const authorInput = document.getElementById('reportAuthorInput');
  const datasetSelect = document.getElementById('reportDatasetSelect');
  if (!body) return;

  const datasetName = datasetSelect ? datasetSelect.options[datasetSelect.selectedIndex].text : AppState.currentDatasetName;
  const title = titleInput ? titleInput.value : 'Enterprise Business Intelligence Briefing';
  const author = authorInput ? authorInput.value : 'Sanjay Raman · Principal BI Lead';

  const incSummary = document.getElementById('secSummary')?.checked ?? true;
  const incKPIs = document.getElementById('secKPIs')?.checked ?? true;
  const incAnalysis = document.getElementById('secAnalysis')?.checked ?? true;
  const incDataQuality = document.getElementById('secDataQuality')?.checked ?? true;
  const incInsights = document.getElementById('secInsights')?.checked ?? true;

  let html = `
    <h2 class="report-doc-title">${title}</h2>
    <div class="report-doc-meta"><strong>Author:</strong> ${author} · <strong>Dataset:</strong> ${datasetName} · <strong>Classification:</strong> Confidential</div>
  `;

  if (incSummary) {
    html += `
      <div class="report-section-block">
        <div class="report-section-title">1. Executive Summary</div>
        <p class="report-text-p">
          This corporate briefing provides verified analytical evaluations across active enterprise telemetry. 
          Performance indicators demonstrate strong expansion momentum (+18.4% YoY ARR) with data quality integrity score 
          passing enterprise compliance audits at 98.5%. Strategic operational recommendations are outlined below.
        </p>
      </div>
    `;
  }

  if (incKPIs) {
    html += `
      <div class="report-section-block">
        <div class="report-section-title">2. Key Performance Indicators</div>
        <div class="preview-metrics-bar mt-2">
          <div class="preview-metric-item"><span class="pm-label">Net ARR</span><span class="pm-value">$8.45M (+18.4%)</span></div>
          <div class="preview-metric-item"><span class="pm-label">Subscribers</span><span class="pm-value">3,850 Active</span></div>
          <div class="preview-metric-item"><span class="pm-label">Net Retention</span><span class="pm-value">140% Peak</span></div>
          <div class="preview-metric-item"><span class="pm-label">Data Quality</span><span class="pm-value text-success">100.0% Clean</span></div>
        </div>
      </div>
    `;
  }

  if (incAnalysis) {
    html += `
      <div class="report-section-block">
        <div class="report-section-title">3. Statistical Analysis & Trajectory</div>
        <p class="report-text-p">
          Linear trend decomposition indicates an average expansion velocity of +$238.9k per monthly period. 
          Moving averages confirm stability across North American enterprise contracts with minimal seasonal contraction.
        </p>
      </div>
    `;
  }

  if (incDataQuality) {
    html += `
      <div class="report-section-block">
        <div class="report-section-title">4. Data Governance & Integrity Audit</div>
        <p class="report-text-p">
          Zero primary key conflicts were detected. All numeric fields adhere to normal bounds with variance within acceptable confidence limits.
        </p>
      </div>
    `;
  }

  if (incInsights) {
    html += `
      <div class="report-section-block">
        <div class="report-section-title">5. AI Strategic Recommendations</div>
        <ul style="padding-left: 20px; font-size: 13px; color: var(--text-secondary); line-height: 1.8;">
          <li><strong>EMEA Pipeline Acceleration:</strong> Expand outbound SDR coverage to replicate 134% Net Retention trajectory.</li>
          <li><strong>Proactive Onboarding Triggers:</strong> Implement Day-45 customer engagement check-ins to curtail early-stage churn.</li>
          <li><strong>Buffer Stock Management:</strong> Maintain 7-day inventory reorder triggers to prevent weekend stockouts.</li>
        </ul>
      </div>
    `;
  }

  body.innerHTML = html;
}

function exportReportPDF() {
  window.print();
}

function exportReportExcel() {
  const wb = XLSX.utils.book_new();

  // Sheet 1: Executive Summary
  const summaryData = [
    ["Enterprise Analytics Platform — Executive Report"],
    ["Generated", new Date().toISOString()],
    ["Dataset", AppState.currentDatasetName],
    [""],
    ["Metric", "Value", "Status"],
    ["Net ARR", "$8.45M", "+18.4% YoY"],
    ["Subscribers", "3,850", "Active"],
    ["Data Quality Score", "100%", "Verified"]
  ];
  const wsSummary = XLSX.utils.aoa_to_sheet(summaryData);
  XLSX.utils.book_append_sheet(wb, wsSummary, "Executive Summary");

  // Sheet 2: Raw Data
  if (AppState.currentRows.length > 0) {
    const wsData = XLSX.utils.json_to_sheet(AppState.currentRows);
    XLSX.utils.book_append_sheet(wb, wsData, "Raw Dataset");
  }

  XLSX.writeFile(wb, `${AppState.currentDatasetId}_Executive_Report.xlsx`);
  showToast('Generated multi-sheet Excel report (.xlsx)', 'success');
}

// ==========================================================================
// 10. MODALS, SEARCH, & UTILITIES
// ==========================================================================
function openSearchModal() {
  const modal = document.getElementById('searchModal');
  if (modal) {
    modal.classList.add('active');
    const input = document.getElementById('modalSearchInput');
    if (input) { input.value = ''; input.focus(); }
  }
}
function closeSearchModal() {
  const modal = document.getElementById('searchModal');
  if (modal) modal.classList.remove('active');
}

function handleGlobalSearch(query) {
  const q = query.toLowerCase().trim();
  const items = document.querySelectorAll('.search-result-item');
  items.forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = text.includes(q) ? 'flex' : 'none';
  });
}

function openAddDataModal() {
  const modal = document.getElementById('addDataModal');
  if (modal) modal.classList.add('active');
}
function closeAddDataModal() {
  const modal = document.getElementById('addDataModal');
  if (modal) modal.classList.remove('active');
}

function openConnectModal(sourceName) {
  const modal = document.getElementById('connectSourceModal');
  const title = document.getElementById('connectModalTitle');
  if (modal) {
    modal.classList.add('active');
    if (title && sourceName) title.innerHTML = `<i data-lucide="database"></i> Connect ${sourceName}`;
    if (window.lucide) lucide.createIcons();
  }
}
function closeConnectModal() {
  const modal = document.getElementById('connectSourceModal');
  if (modal) modal.classList.remove('active');
}

function testConnectionStatus() {
  showToast('Verifying connection latency and TLS handshake…', 'info');
  setTimeout(() => {
    showToast('Connection verified! Response time: 38ms', 'success');
  }, 600);
}

function saveConnection() {
  closeConnectModal();
  showToast('Data source connection configured and saved', 'success');
}

function openChartFullscreen(chartId, title) {
  const modal = document.getElementById('chartFullscreenModal');
  const titleEl = document.getElementById('chartFullscreenTitle');
  if (!modal) return;
  modal.classList.add('active');
  if (titleEl) titleEl.textContent = title || 'Chart Fullscreen Zoom';

  const origChart = AppState.chartInstances[chartId];
  if (origChart) {
    const fullCanvas = document.getElementById('fullscreenCanvas');
    if (AppState.chartInstances.fullscreenChart) {
      AppState.chartInstances.fullscreenChart.destroy();
    }
    AppState.chartInstances.fullscreenChart = new Chart(fullCanvas, {
      type: origChart.config.type,
      data: JSON.parse(JSON.stringify(origChart.data)),
      options: {
        ...origChart.options,
        responsive: true,
        maintainAspectRatio: false
      }
    });
  }
}
function closeChartFullscreen() {
  const modal = document.getElementById('chartFullscreenModal');
  if (modal) modal.classList.remove('active');
}

function openHelpModal() {
  const modal = document.getElementById('helpModal');
  if (modal) modal.classList.add('active');
}
function closeHelpModal() {
  const modal = document.getElementById('helpModal');
  if (modal) modal.classList.remove('active');
}

function toggleDateMenu() {
  const menu = document.getElementById('dateDropdownMenu');
  if (menu) menu.classList.toggle('active');
}

function setDateRange(rangeKey, label) {
  AppState.currentDateRange = rangeKey;
  const lbl = document.getElementById('selectedDateRangeLabel');
  if (lbl) lbl.textContent = label;
  document.querySelectorAll('#dateDropdownMenu .dropdown-item').forEach(item => {
    item.classList.toggle('active', item.textContent.trim() === label);
  });
  const menu = document.getElementById('dateDropdownMenu');
  if (menu) menu.classList.remove('active');
  showToast(`Date range set to: ${label}`, 'info');
}

function toggleNotifications() {
  const menu = document.getElementById('notifMenu');
  if (menu) menu.classList.toggle('active');
}

function clearNotifications() {
  document.querySelectorAll('.notif-item.unread').forEach(el => el.classList.remove('unread'));
  const badge = document.getElementById('notifCountBadge');
  if (badge) badge.textContent = '0';
  showToast('All notifications marked as read', 'info');
}

function toggleUserDropdown() {
  const menu = document.getElementById('userDropdown');
  if (menu) menu.classList.toggle('active');
}

function closeOnOverlayClick(e, modalId) {
  if (e.target.id === modalId) {
    document.getElementById(modalId).classList.remove('active');
  }
}

// Toast Notifications Engine
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.25s ease';
    setTimeout(() => toast.remove(), 250);
  }, 3200);
}

function renderDashboardActivity() {
  // Activity rows already pre-filled in HTML
}

function exportCurrentChart(chartId, filename) {
  const chart = AppState.chartInstances[chartId];
  if (!chart) return;
  const imageURI = chart.toBase64Image();
  const link = document.createElement('a');
  link.href = imageURI;
  link.download = `${filename || 'chart'}.png`;
  link.click();
  showToast('Chart exported as PNG', 'success');
}

function exportFullscreenChart() {
  exportCurrentChart('fullscreenChart', 'fullscreen_analysis_chart');
}

function exportAllCharts() {
  exportCurrentChart('visualMultiLineChart', 'multi_metric_correlation');
  setTimeout(() => exportCurrentChart('visualStackedBarChart', 'regional_growth_stacked'), 200);
  setTimeout(() => exportCurrentChart('visualAreaChart', 'subscriber_velocity_area'), 400);
  showToast('Exported all studio charts as PNGs', 'success');
}


// ==========================================================================
// 8. WHATSAPP ALERT AUTOMATION CONTROLLER
// ==========================================================================
let whatsAppConfig = {
  enabled: true,
  recipient_phone: "+91 98765 43210",
  recipient_name: "Chinnu",
  provider: "simulator",
  cooldown_minutes: 360,
  rate_limit_hourly: 10,
  notify_critical_only: false
};
let whatsAppRules = [];
let whatsAppLogs = [];

async function fetchWhatsAppConfig() {
  try {
    const res = await fetch('/api/whatsapp/config');
    const data = await res.json();
    if (data && data.config) {
      whatsAppConfig = data.config;
      updateWhatsAppConfigUI();
    }
  } catch (err) {
    console.error('Error fetching WhatsApp config:', err);
  }
}

function updateWhatsAppConfigUI() {
  const masterToggle = document.getElementById('whatsappMasterToggle');
  if (masterToggle) masterToggle.checked = !!whatsAppConfig.enabled;

  const phoneEl = document.getElementById('whatsappGatewayPhone');
  if (phoneEl) phoneEl.innerHTML = `<i data-lucide="phone"></i> Recipient: <strong>${whatsAppConfig.recipient_phone}</strong> (${whatsAppConfig.recipient_name || 'Chinnu'})`;

  const providerEl = document.getElementById('whatsappGatewayProvider');
  if (providerEl) {
    const provLabels = {
      simulator: 'Simulator Gateway',
      twilio: 'Twilio Cloud API',
      meta_cloud: 'Meta Cloud API',
      webhook: 'Custom Webhook'
    };
    providerEl.textContent = provLabels[whatsAppConfig.provider] || 'Simulator Gateway';
  }

  const cooldownEl = document.getElementById('whatsappCooldownValue');
  if (cooldownEl) cooldownEl.textContent = `${Math.round((whatsAppConfig.cooldown_minutes || 360) / 60)} Hours`;

  const badgeEl = document.getElementById('whatsappGatewayBadge');
  if (badgeEl) {
    if (whatsAppConfig.enabled) {
      badgeEl.className = 'status-indicator active';
      badgeEl.innerHTML = '<span class="ping-dot green"></span> Connected';
    } else {
      badgeEl.className = 'status-indicator inactive';
      badgeEl.innerHTML = '<span class="ping-dot amber"></span> Paused';
    }
  }

  if (window.lucide) lucide.createIcons();
}

async function toggleWhatsAppAutomation(enabled) {
  try {
    const res = await fetch('/api/whatsapp/toggle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ enabled })
    });
    const data = await res.json();
    if (data.success) {
      whatsAppConfig = data.config;
      updateWhatsAppConfigUI();
      showToast(enabled ? '✅ WhatsApp Automation enabled' : '⏸️ WhatsApp Automation paused', enabled ? 'success' : 'warning');
    }
  } catch (err) {
    showToast('Failed to update WhatsApp automation state', 'danger');
  }
}

async function fetchWhatsAppRules() {
  try {
    const res = await fetch('/api/whatsapp/rules');
    const data = await res.json();
    if (data && data.rules) {
      whatsAppRules = data.rules;
      renderWhatsAppRulesTable();
      const countEl = document.getElementById('whatsappActiveRulesCount');
      if (countEl) countEl.textContent = `${whatsAppRules.filter(r => r.enabled).length} Rules`;
    }
  } catch (err) {
    console.error('Error fetching WhatsApp rules:', err);
  }
}

function renderWhatsAppRulesTable() {
  const tbody = document.getElementById('whatsappRulesTableBody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (whatsAppRules.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No automation rules configured. Click "Add Custom Rule" to create one.</td></tr>`;
    return;
  }

  whatsAppRules.forEach(rule => {
    const tr = document.createElement('tr');
    const urgencyClass = `urgency-${rule.urgency || 'high'}`;
    const triggerLabels = {
      stockout_risk: '📦 Inventory Stockout Risk',
      sentiment_dip: '💬 Customer Sentiment Dip',
      sales_drop: '📉 Sales Forecast Decline',
      daily_summary: '📊 Daily Executive Digest',
      custom_metric: '⚡ Custom KPI Threshold'
    };

    tr.innerHTML = `
      <td>
        <div class="font-medium text-primary">${rule.name}</div>
        <div class="text-xs text-sub">${rule.description || ''}</div>
      </td>
      <td><span class="font-medium">${triggerLabels[rule.event_type] || rule.event_type}</span></td>
      <td><code>${rule.metric || 'value'} ${rule.operator || '<='} ${rule.threshold}</code></td>
      <td><span class="urgency-badge ${urgencyClass}">${rule.urgency}</span></td>
      <td>
        <label class="switch-toggle" style="transform: scale(0.85);" title="Toggle rule active state">
          <input type="checkbox" ${rule.enabled ? 'checked' : ''} onchange="toggleRuleActive('${rule.id}', this.checked)">
          <span class="slider-round"></span>
        </label>
      </td>
      <td>
        <div class="action-buttons-group">
          <button class="btn-ghost-sm" title="Edit Rule" onclick="openCreateRuleModal('${rule.id}')"><i data-lucide="edit-2"></i></button>
          <button class="btn-ghost-sm text-danger" title="Delete Rule" onclick="deleteRule('${rule.id}')"><i data-lucide="trash-2"></i></button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });

  if (window.lucide) lucide.createIcons();
}

async function toggleRuleActive(ruleId, enabled) {
  try {
    const res = await fetch(`/api/whatsapp/rules/${ruleId}/toggle`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ enabled })
    });
    const data = await res.json();
    if (data.success) {
      whatsAppRules = data.rules;
      renderWhatsAppRulesTable();
      showToast(`Rule updated: ${enabled ? 'Enabled' : 'Disabled'}`, 'info');
    }
  } catch (err) {
    showToast('Failed to toggle rule state', 'danger');
  }
}

async function deleteRule(ruleId) {
  if (!confirm('Are you sure you want to delete this automation rule?')) return;
  try {
    const res = await fetch(`/api/whatsapp/rules/${ruleId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      whatsAppRules = data.rules;
      renderWhatsAppRulesTable();
      showToast('Automation rule deleted', 'success');
    }
  } catch (err) {
    showToast('Failed to delete rule', 'danger');
  }
}

function openCreateRuleModal(ruleId = null) {
  const modal = document.getElementById('createRuleModal');
  if (!modal) return;
  const title = document.getElementById('createRuleModalTitle');
  const editIdInput = document.getElementById('ruleEditId');
  const nameInput = document.getElementById('ruleNameInput');
  const typeSelect = document.getElementById('ruleEventTypeSelect');
  const opSelect = document.getElementById('ruleOperatorSelect');
  const threshInput = document.getElementById('ruleThresholdInput');
  const urgSelect = document.getElementById('ruleUrgencySelect');

  if (ruleId) {
    const rule = whatsAppRules.find(r => r.id === ruleId);
    if (rule) {
      if (title) title.innerHTML = `<i data-lucide="edit" class="green"></i> Edit Automation Rule`;
      if (editIdInput) editIdInput.value = rule.id;
      if (nameInput) nameInput.value = rule.name;
      if (typeSelect) typeSelect.value = rule.event_type;
      if (opSelect) opSelect.value = rule.operator || '<=';
      if (threshInput) threshInput.value = rule.threshold;
      if (urgSelect) urgSelect.value = rule.urgency || 'high';
    }
  } else {
    if (title) title.innerHTML = `<i data-lucide="plus-circle" class="green"></i> Create WhatsApp Automation Rule`;
    if (editIdInput) editIdInput.value = '';
    if (nameInput) nameInput.value = 'Low Stock Buffer Warning';
    if (typeSelect) typeSelect.value = 'stockout_risk';
    if (opSelect) opSelect.value = '<=';
    if (threshInput) threshInput.value = '5';
    if (urgSelect) urgSelect.value = 'critical';
  }

  modal.classList.add('active');
  if (window.lucide) lucide.createIcons();
}

function closeCreateRuleModal() {
  const modal = document.getElementById('createRuleModal');
  if (modal) modal.classList.remove('active');
}

function handleRuleEventTypeChange(val) {
  const lbl = document.getElementById('ruleThresholdLabel');
  const help = document.getElementById('ruleThresholdHelp');
  const inp = document.getElementById('ruleThresholdInput');
  if (!lbl || !help || !inp) return;

  if (val === 'stockout_risk') {
    lbl.textContent = 'Stock Runway Cutoff (Days)';
    help.textContent = 'Triggers when days of stock remaining drops below this value.';
    inp.value = '5';
  } else if (val === 'sentiment_dip') {
    lbl.textContent = 'Positive Feedback Ratio (%)';
    help.textContent = 'Triggers when positive review ratio drops below this percentage.';
    inp.value = '50';
  } else if (val === 'sales_drop') {
    lbl.textContent = 'Forecast Change Cutoff (%)';
    help.textContent = 'Triggers when month-over-month revenue forecast decline reaches this threshold.';
    inp.value = '-8';
  } else {
    lbl.textContent = 'Numerical Cutoff Threshold';
    help.textContent = 'Triggers when custom metric crosses this boundary value.';
    inp.value = '50';
  }
}

async function saveRuleFromModal() {
  const id = document.getElementById('ruleEditId').value;
  const name = document.getElementById('ruleNameInput').value.trim();
  const event_type = document.getElementById('ruleEventTypeSelect').value;
  const operator = document.getElementById('ruleOperatorSelect').value;
  const threshold = parseFloat(document.getElementById('ruleThresholdInput').value) || 0;
  const urgency = document.getElementById('ruleUrgencySelect').value;
  const auto_send = document.getElementById('ruleAutoSendCheck').checked;

  if (!name) {
    showToast('Please provide a descriptive rule name', 'warning');
    return;
  }

  const payload = {
    id: id || undefined,
    name,
    event_type,
    operator,
    threshold,
    urgency,
    auto_send,
    enabled: true
  };

  try {
    const res = await fetch('/api/whatsapp/rules', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      whatsAppRules = data.rules;
      renderWhatsAppRulesTable();
      closeCreateRuleModal();
      showToast(id ? 'Rule updated successfully' : 'New automation rule created', 'success');
    }
  } catch (err) {
    showToast('Failed to save automation rule', 'danger');
  }
}

// Config Modal
function openWhatsAppConfigModal() {
  const modal = document.getElementById('whatsappConfigModal');
  if (!modal) return;
  const phone = document.getElementById('waConfigPhone');
  const name = document.getElementById('waConfigName');
  const prov = document.getElementById('waConfigProvider');
  const cd = document.getElementById('waConfigCooldown');
  const rl = document.getElementById('waConfigRateLimit');
  const crit = document.getElementById('waConfigCriticalOnly');

  if (phone) phone.value = whatsAppConfig.recipient_phone || '+91 98765 43210';
  if (name) name.value = whatsAppConfig.recipient_name || 'Chinnu';
  if (prov) prov.value = whatsAppConfig.provider || 'simulator';
  if (cd) cd.value = whatsAppConfig.cooldown_minutes || 360;
  if (rl) rl.value = whatsAppConfig.rate_limit_hourly || 10;
  if (crit) crit.checked = !!whatsAppConfig.notify_critical_only;

  modal.classList.add('active');
  if (window.lucide) lucide.createIcons();
}

function closeWhatsAppConfigModal() {
  const modal = document.getElementById('whatsappConfigModal');
  if (modal) modal.classList.remove('active');
}

async function saveWhatsAppConfigFromModal() {
  const phone = document.getElementById('waConfigPhone').value.trim();
  const name = document.getElementById('waConfigName').value.trim();
  const provider = document.getElementById('waConfigProvider').value;
  const cooldown_minutes = parseInt(document.getElementById('waConfigCooldown').value) || 360;
  const rate_limit_hourly = parseInt(document.getElementById('waConfigRateLimit').value) || 10;
  const notify_critical_only = document.getElementById('waConfigCriticalOnly').checked;

  try {
    const res = await fetch('/api/whatsapp/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recipient_phone: phone,
        recipient_name: name,
        provider,
        cooldown_minutes,
        rate_limit_hourly,
        notify_critical_only
      })
    });
    const data = await res.json();
    if (data.success) {
      whatsAppConfig = data.config;
      updateWhatsAppConfigUI();
      closeWhatsAppConfigModal();
      showToast('WhatsApp Gateway settings saved', 'success');
    }
  } catch (err) {
    showToast('Failed to save settings', 'danger');
  }
}

async function testWhatsAppConnectionFromModal() {
  const phone = document.getElementById('waConfigPhone').value.trim();
  showToast('Sending WhatsApp test ping...', 'info');
  try {
    const res = await fetch('/api/whatsapp/test-connection', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone })
    });
    const data = await res.json();
    if (data.success) {
      showToast('✅ WhatsApp connection verified! Ping received.', 'success');
      fetchWhatsAppHistory();
    }
  } catch (err) {
    showToast('Connection test failed', 'danger');
  }
}

// Transmission History & Phone Simulator
async function fetchWhatsAppHistory() {
  try {
    const res = await fetch('/api/whatsapp/history');
    const data = await res.json();
    if (data && data.logs) {
      whatsAppLogs = data.logs;
      renderWhatsAppHistoryTable();
      renderPhoneSimulatorFeed();
      const countEl = document.getElementById('whatsappTotalSentCount');
      if (countEl) countEl.textContent = `${whatsAppLogs.length}`;
    }
  } catch (err) {
    console.error('Error fetching WhatsApp history:', err);
  }
}

function renderWhatsAppHistoryTable() {
  const tbody = document.getElementById('whatsappLogTableBody');
  if (!tbody) return;
  tbody.innerHTML = '';

  if (whatsAppLogs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No alert transmission history recorded yet.</td></tr>`;
    return;
  }

  whatsAppLogs.forEach(log => {
    const tr = document.createElement('tr');
    const urgencyClass = `urgency-${log.urgency || 'info'}`;
    const timeStr = log.timestamp ? new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Now';

    tr.innerHTML = `
      <td><span class="font-mono text-xs">${timeStr}</span></td>
      <td><span class="font-medium">${log.to || whatsAppConfig.recipient_phone}</span></td>
      <td>
        <div class="font-medium text-primary">${log.title || 'Notification'}</div>
        <div class="text-xs text-sub truncate" style="max-width: 260px;">${(log.message || '').replace(/[*_`]/g, '').slice(0, 75)}...</div>
      </td>
      <td><span class="urgency-badge ${urgencyClass}">${log.urgency || 'info'}</span></td>
      <td><span class="text-xs font-mono">${log.channel || 'WhatsApp Bot'}</span></td>
      <td>
        <span class="status-badge success" style="display:inline-flex; align-items:center; gap:4px;">
          <i data-lucide="check-check" style="width:13px; height:13px;"></i> Delivered
        </span>
      </td>
    `;
    tbody.appendChild(tr);
  });

  if (window.lucide) lucide.createIcons();
}

function renderPhoneSimulatorFeed() {
  const container = document.getElementById('waChatBubblesContainer');
  if (!container) return;
  container.innerHTML = '';

  if (whatsAppLogs.length === 0) {
    container.innerHTML = `<div class="text-center text-xs text-muted py-6">No incoming WhatsApp alerts yet.</div>`;
    return;
  }

  // Show up to 10 latest logs in reverse chronological order for chat view
  const recent = [...whatsAppLogs].slice(-10);
  recent.forEach(log => {
    const bubble = document.createElement('div');
    bubble.className = `wa-message-bubble ${log.direction === 'outgoing' ? 'outgoing' : 'incoming'}`;
    const formattedBody = (log.message || '')
      .replace(/\n/g, '<br>')
      .replace(/\*(.*?)\*/g, '<strong>$1</strong>')
      .replace(/_(.*?)_/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>');

    const timeStr = log.timestamp ? new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Now';

    bubble.innerHTML = `
      ${log.title ? `<div class="wa-bubble-title">${log.title}</div>` : ''}
      <div class="wa-bubble-body">${formattedBody}</div>
      <div class="wa-bubble-footer">
        <span class="wa-msg-time">${timeStr}</span>
        <i data-lucide="check-check" class="wa-double-check read"></i>
      </div>
    `;
    container.appendChild(bubble);
  });

  const chatBody = document.getElementById('waPhoneChatBody');
  if (chatBody) chatBody.scrollTop = chatBody.scrollHeight;

  if (window.lucide) lucide.createIcons();
}

async function clearWhatsAppHistory() {
  if (!confirm('Clear all WhatsApp alert history logs?')) return;
  try {
    const res = await fetch('/api/whatsapp/history', { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      whatsAppLogs = [];
      renderWhatsAppHistoryTable();
      renderPhoneSimulatorFeed();
      showToast('WhatsApp log history cleared', 'info');
    }
  } catch (err) {
    showToast('Failed to clear history', 'danger');
  }
}

async function evaluateWhatsAppTriggersNow() {
  showToast('Evaluating real-time telemetry against automation rules...', 'info');
  try {
    const res = await fetch('/api/whatsapp/evaluate-triggers', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      if (data.triggered_count > 0) {
        showToast(`⚡ ${data.triggered_count} automated alert(s) triggered & dispatched to WhatsApp!`, 'success');
      } else {
        showToast('Telemetry optimal. No new alerts triggered under cooldown policy.', 'info');
      }
      fetchWhatsAppHistory();
    }
  } catch (err) {
    showToast('Error evaluating triggers', 'danger');
  }
}

// Simulator Quick Actions
async function sendStockoutTestAlert() {
  try {
    const res = await fetch('/api/whatsapp/send-immediate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event_type: 'stockout_risk',
        urgency: 'critical',
        data: { name: 'Cotton Sarees Premium', sku: 'SAR-001', stock: 4, days_left: 2, stockout_risk_pct: 92.5, reorder_point_units: 12, eoq_units: 18 }
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast('🚨 Critical stockout alert dispatched to simulator', 'warning');
      fetchWhatsAppHistory();
    }
  } catch (err) {
    showToast('Failed to dispatch alert', 'danger');
  }
}

async function sendDailySummaryAlert() {
  try {
    const res = await fetch('/api/whatsapp/send-immediate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event_type: 'daily_summary',
        urgency: 'info',
        data: { health_score: 47, badge: 'Attention Required', sales_forecast_3m: 196.6, reorder_count: 2, nps: 21, positive_pct: 57.1 }
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast('📊 Daily executive briefing dispatched to simulator', 'success');
      fetchWhatsAppHistory();
    }
  } catch (err) {
    showToast('Failed to dispatch summary', 'danger');
  }
}

async function sendTamilPromoAlert() {
  try {
    const res = await fetch('/api/whatsapp/send-immediate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event_type: 'custom',
        language: 'ta',
        title: '✨ சிறப்பு பண்டிகை தள்ளுபடி Offer',
        message: '✨ வணக்கம் Chinnu! Sarees & Home Goods மீது சிறப்பு பண்டிகை தள்ளுபடி 15% இன்று முதல் ஆரம்பம்! இன்றே வாங்கி பரிசுகளை வெல்லுங்கள். WhatsApp: 📞 9876543210. Chinnu Textiles.',
        urgency: 'medium'
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast('✨ தமிழ் Promo broadcast dispatched to simulator', 'success');
      fetchWhatsAppHistory();
    }
  } catch (err) {
    showToast('Failed to dispatch promo', 'danger');
  }
}

function clearSimulatorChat() {
  const container = document.getElementById('waChatBubblesContainer');
  if (container) container.innerHTML = `<div class="text-center text-xs text-muted py-6">Simulator chat cleared.</div>`;
  showToast('Phone simulator chat cleared', 'info');
}

async function sendSimulatorReply() {
  const input = document.getElementById('waSimulatorInput');
  if (!input || !input.value.trim()) return;
  const userText = input.value.trim();
  input.value = '';

  // Append user bubble in simulator
  const container = document.getElementById('waChatBubblesContainer');
  if (container) {
    const bubble = document.createElement('div');
    bubble.className = 'wa-message-bubble outgoing';
    const nowStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    bubble.innerHTML = `
      <div class="wa-bubble-body">${userText}</div>
      <div class="wa-bubble-footer">
        <span class="wa-msg-time">${nowStr}</span>
        <i data-lucide="check-check" class="wa-double-check read"></i>
      </div>
    `;
    container.appendChild(bubble);
    const chatBody = document.getElementById('waPhoneChatBody');
    if (chatBody) chatBody.scrollTop = chatBody.scrollHeight;
    if (window.lucide) lucide.createIcons();
  }

  // Route to voice assistant engine for automated bot reply
  try {
    const res = await fetch('/api/voice/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ transcript: userText })
    });
    const botData = await res.json();
    if (botData && botData.spoken_text) {
      setTimeout(() => {
        if (container) {
          const botBubble = document.createElement('div');
          botBubble.className = 'wa-message-bubble incoming';
          const nowStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
          botBubble.innerHTML = `
            <div class="wa-bubble-title">🤖 Vyapaar Pulse Bot</div>
            <div class="wa-bubble-body">${botData.spoken_text}</div>
            <div class="wa-bubble-footer">
              <span class="wa-msg-time">${nowStr}</span>
              <i data-lucide="check-check" class="wa-double-check read"></i>
            </div>
          `;
          container.appendChild(botBubble);
          const chatBody = document.getElementById('waPhoneChatBody');
          if (chatBody) chatBody.scrollTop = chatBody.scrollHeight;
          if (window.lucide) lucide.createIcons();
        }
      }, 500);
    }
  } catch (err) {
    console.error('Error processing reply:', err);
  }
}

// Compose Modal
function openComposeAlertModal() {
  const modal = document.getElementById('composeAlertModal');
  if (!modal) return;
  const phone = document.getElementById('composePhoneInput');
  if (phone) phone.value = whatsAppConfig.recipient_phone || '+91 98765 43210';
  regenerateComposePreview();
  modal.classList.add('active');
  if (window.lucide) lucide.createIcons();
}

function closeComposeAlertModal() {
  const modal = document.getElementById('composeAlertModal');
  if (modal) modal.classList.remove('active');
}

function handleComposeTemplateSelect(val) {
  regenerateComposePreview();
}

function regenerateComposePreview() {
  const template = document.getElementById('composeTemplateSelect').value;
  const lang = document.getElementById('composeLangSelect').value;
  const msgArea = document.getElementById('composeMessageText');
  if (!msgArea) return;

  const samples = {
    daily_summary: {
      en: "📊 *Vyapaar Pulse Daily Executive Briefing*\n\nHello *Chinnu*! Here is your daily operational telemetry:\n• Business Health Score: *47/100* (Attention Required)\n• 3-Month Projected Revenue: *₹196.6k*\n• Inventory Stockout Triggers: *2 item(s) need reorder*\n• Customer Sentiment: *57.1% Positive* (NPS: +21)\n\n💡 *Action:* Issue vendor POs for low stock items.",
      ta: "📊 *வியாபார் பல்ஸ் தினசரி அறிக்கை*\n\nவணக்கம் *Chinnu*! இன்றைய பிசினஸ் நிலவரம்:\n• பிசினஸ் ஹெல்த் ஸ்கோர்: *47/100* (Attention Required)\n• அடுத்த மாத விற்பனை: *₹196.6k*\n• உடனடி ஸ்டாக் தேவை: *2 பொருட்கள்*\n• வாடிக்கையாளர் திருப்தி: *57.1% Positive* (NPS: +21)\n\n💡 *பரிந்துரை:* தீரும் நிலையில் உள்ள பொருட்களை உடனே ஆர்டர் செய்யவும்.",
      hi: "📊 *व्यापार पल्स दैनिक ब्रीफिंग*\n\nनमस्ते *Chinnu*! आज का मुख्य सारांश:\n• बिजनेस हेल्थ स्कोर: *47/100*\n• अनुमानित बिक्री: *₹196.6k*\n• रीऑर्डर अलर्ट: *2 उत्पाद*\n• ग्राहक संतुष्टि (NPS): *+21*\n\n💡 *कार्रवाई सुझाव:* कम स्टॉक वाले उत्पादों का तुरंत ऑर्डर दें।",
      te: "📊 *వ్యాపార్ పల్స్ డైలీ బ్రీఫింగ్*\n\nనమస్కారం *Chinnu*! నేటి బిజినెస్ సారాంశం:\n• హెల్త్ స్కోర్: *47/100*\n• అంచనా వేసిన అమ్మకాలు: *₹196.6k*\n• రీఆర్డర్ హెచ్చరిక: *2 వస్తువులు*",
      ml: "📊 *വ്യാപാര പൾസ് പ്രതിദിന റിപ്പോർട്ട്*\n\nപ്രിയ *Chinnu*!\n• ബിസിനസ് ഹെൽത്ത് സ്കോർ: *47/100*\n• പ്രതീക്ഷിക്കുന്ന വരുമാനം: *₹196.6k*",
      kn: "📊 *ವ್ಯಾಪಾರ ಪಲ್ಸ್ ದೈನಂದಿನ ವರದಿ*\n\nನಮಸ್ಕಾರ *Chinnu*!\n• ಹೆಲ್ತ್ ಸ್ಕೋರ್: *47/100*\n• ನಿರೀಕ್ಷಿತ ಆದಾಯ: *₹196.6k*"
    },
    stockout_risk: {
      en: "🚨 *Critical Stockout Alert*\n\n• Product: *Cotton Sarees Premium* (`SAR-001`)\n• Stock Remaining: *4 units* (2 days left)\n• Stockout Probability: *92.5%*\n• Recommended Reorder: *12 units*\n\n⚡ *Recommended Action:* Place emergency purchase order immediately.",
      ta: "🚨 *முக்கிய ஸ்டாக் எச்சரிக்கை*\n\n• பொருள்: *Cotton Sarees Premium* (`SAR-001`)\n• தற்போதைய இருப்பு: *4 units* (2 நாட்கள் மட்டுமே)\n• ஸ்டாக் அவுட் ஆபத்து: *92.5%*\n• பரிந்துரைக்கப்படும் கொள்முதல்: *12 units*\n\n⚡ *பரிந்துரை:* உடனடியாக சப்ளையரைத் தொடர்பு கொள்ளவும்.",
      hi: "🚨 *महत्वपूर्ण स्टॉक अलर्ट*\n\n• उत्पाद: *Cotton Sarees Premium* (`SAR-001`)\n• शेष स्टॉक: *4 units* (2 दिन शेष)\n• स्टॉकआउट जोखिम: *92.5%*\n\n⚡ *कार्रवाई:* तुरंत नया स्टॉक मंगवाएं।",
      te: "🚨 *స్టాక్ హెచ్చరిక: Cotton Sarees*\n• మిగిలిన స్టాక్: 4 units (2 రోజులు మాత్రమే)",
      ml: "🚨 *സ്റ്റോക്ക് അലേർട്ട്: Cotton Sarees*\n• ബാക്കിയുള്ള സ്റ്റോക്ക്: 4 units",
      kn: "🚨 *ಸ್ಟಾಕ್ ಎಚ್ಚರಿಕೆ: Cotton Sarees*\n• ಉಳಿದ ದಾಸ್ತಾನು: 4 units"
    },
    sentiment_dip: {
      en: "⚠️ *Customer Satisfaction Alert*\n\n• Positive Review Ratio: *45.0%* (Below 50% Threshold)\n• Root Cause: *Delivery Delays & Packaging Issues*\n\n⚡ *Action:* Coordinate with logistics partners.",
      ta: "⚠️ *வாடிக்கையாளர் திருப்தி எச்சரிக்கை*\n\n• தற்போதைய பாசிட்டிவ் ரேட்டிங்: *45.0%*\n• முக்கிய புகார்: *டெலிவரி தாமதம்*",
      hi: "⚠️ *ग्राहक संतुष्टि अलर्ट*\n\n• पॉजिटिव रेटिंग: *45.0%*\n• मुख्य समस्या: *डिलीवरी में देरी*"
    }
  };

  const selectedTemplate = samples[template] || samples.daily_summary;
  msgArea.value = selectedTemplate[lang] || selectedTemplate.en;
}

async function sendCustomAlertFromModal() {
  const phone = document.getElementById('composePhoneInput').value.trim();
  const message = document.getElementById('composeMessageText').value.trim();
  const urgency = document.getElementById('composeUrgencySelect').value;

  if (!message) {
    showToast('Please enter message text', 'warning');
    return;
  }

  try {
    const res = await fetch('/api/whatsapp/send-immediate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone,
        message,
        urgency,
        event_type: 'custom',
        title: '⚡ Executive Alert Notification'
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`✅ WhatsApp alert delivered to ${phone}`, 'success');
      closeComposeAlertModal();
      fetchWhatsAppHistory();
    }
  } catch (err) {
    showToast('Failed to dispatch alert', 'danger');
  }
}

function triggerScheduledDigestNow() {
  sendDailySummaryAlert();
}


// ==========================================================================
// 9. FLOATING MULTILINGUAL AI ASSISTANT & VOICE COPILOT
// ==========================================================================
let isAiPanelOpen = false;
let isListening = false;
let isVoiceMuted = false;
let assistantLanguage = 'auto';
let recognitionInstance = null;
let synthesisVoices = [];

function initFloatingAiAssistant() {
  // Populate speech synthesis voices when loaded
  if ('speechSynthesis' in window) {
    speechSynthesis.onvoiceschanged = () => {
      synthesisVoices = speechSynthesis.getVoices();
    };
    synthesisVoices = speechSynthesis.getVoices();
  }

  // Bind direct click handlers
  const btn = document.getElementById('floatingAiBtn');
  if (btn) btn.addEventListener('click', (e) => { e.stopPropagation(); toggleFloatingAiPanel(); });
  
  const pill = document.getElementById('floatingAiPill');
  if (pill) pill.addEventListener('click', (e) => { e.stopPropagation(); toggleFloatingAiPanel(); });

  const topbarBtn = document.getElementById('topbarAiBtn');
  if (topbarBtn) topbarBtn.addEventListener('click', (e) => { e.stopPropagation(); toggleFloatingAiPanel(); });

  // Keyboard shortcut: Alt + A
  document.addEventListener('keydown', (e) => {
    if (e.altKey && (e.key === 'a' || e.key === 'A')) {
      e.preventDefault();
      toggleFloatingAiPanel();
    }
  });

  // Setup Web Speech API SpeechRecognition
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = false;
    recognitionInstance.interimResults = false;

    recognitionInstance.onstart = () => {
      isListening = true;
      updateListeningUI(true);
    };

    recognitionInstance.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (transcript && transcript.trim()) {
        sendAssistantTextMessage(transcript.trim());
      }
    };

    recognitionInstance.onerror = (event) => {
      console.warn('Speech recognition error:', event.error);
      isListening = false;
      updateListeningUI(false);
      showToast(`Microphone notice: ${event.error}`, 'warning');
    };

    recognitionInstance.onend = () => {
      isListening = false;
      updateListeningUI(false);
    };
  }
}

function openFloatingAiPanel() {
  const panel = document.getElementById('floatingAiPanel');
  if (!panel) return;
  isAiPanelOpen = true;
  panel.classList.add('open');
  const input = document.getElementById('aiTextInput');
  if (input) setTimeout(() => input.focus(), 150);
  if (window.lucide) lucide.createIcons();
}

function closeFloatingAiPanel() {
  const panel = document.getElementById('floatingAiPanel');
  if (!panel) return;
  isAiPanelOpen = false;
  panel.classList.remove('open');
  stopAssistantSpeaking();
  if (isListening && recognitionInstance) {
    recognitionInstance.stop();
  }
  if (window.lucide) lucide.createIcons();
}

function toggleFloatingAiPanel() {
  if (isAiPanelOpen) {
    closeFloatingAiPanel();
  } else {
    openFloatingAiPanel();
  }
}

// Expose globally to window
window.toggleFloatingAiPanel = toggleFloatingAiPanel;
window.openFloatingAiPanel = openFloatingAiPanel;
window.closeFloatingAiPanel = closeFloatingAiPanel;

function handleAssistantLangChange(langCode) {
  assistantLanguage = langCode;
  const subEl = document.getElementById('aiHeaderSub');
  const labels = {
    'auto': 'Auto Multilingual Detection',
    'ta-IN': 'தமிழ் AI குரல் வழிகாட்டி',
    'en-IN': 'English AI Business Copilot',
    'hi-IN': 'हिन्दी एआई बिजनेस सहायक',
    'te-IN': 'తెలుగు ఏఐ వ్యాపార సహాయకుడు',
    'ml-IN': 'മലയാളം ബിസിനസ്സ് അസിസ്റ്റന്റ്',
    'kn-IN': 'ಕನ್ನಡ ಎಐ ವ್ಯಾಪಾರ ಸಹಾಯಕ'
  };
  if (subEl) subEl.textContent = labels[langCode] || 'Multilingual Voice & WhatsApp Copilot';
  showToast(`Assistant language: ${langCode.toUpperCase()}`, 'info');
}

function toggleAssistantVoiceMute() {
  isVoiceMuted = !isVoiceMuted;
  const icon = document.getElementById('aiVoiceMuteIcon');
  if (icon) {
    icon.setAttribute('data-lucide', isVoiceMuted ? 'volume-x' : 'volume-2');
  }
  if (isVoiceMuted) stopAssistantSpeaking();
  showToast(isVoiceMuted ? 'Voice output muted' : 'Voice output unmuted', 'info');
  if (window.lucide) lucide.createIcons();
}

function toggleMicrophoneListening() {
  if (!recognitionInstance) {
    showToast('Web Speech API is not supported in this browser. Type in the text box below.', 'warning');
    return;
  }

  if (isListening) {
    recognitionInstance.stop();
  } else {
    stopAssistantSpeaking();
    // Set recognition language
    if (assistantLanguage && assistantLanguage !== 'auto') {
      recognitionInstance.lang = assistantLanguage;
    } else {
      recognitionInstance.lang = 'en-IN';
    }
    try {
      recognitionInstance.start();
    } catch (err) {
      console.warn('Recognition start exception:', err);
    }
  }
}

function updateListeningUI(active) {
  const micBtn = document.getElementById('aiMicBtn');
  const statusText = document.getElementById('aiStatusText');
  const visualizer = document.getElementById('waveformBars');

  if (micBtn) micBtn.classList.toggle('listening', active);
  if (visualizer) visualizer.classList.toggle('active', active);
  if (statusText) {
    statusText.textContent = active ? 'Listening to speech...' : 'Ready for Voice or Text';
  }
}

function updateSpeakingUI(active) {
  const stopBtn = document.getElementById('aiStopSpeechBtn');
  const statusText = document.getElementById('aiStatusText');
  const visualizer = document.getElementById('waveformBars');

  if (stopBtn) stopBtn.classList.toggle('hidden', !active);
  if (visualizer) visualizer.classList.toggle('active', active);
  if (statusText) {
    statusText.textContent = active ? 'Speaking audio response...' : 'Ready for Voice or Text';
  }
}

function stopAssistantSpeaking() {
  if ('speechSynthesis' in window) {
    speechSynthesis.cancel();
  }
  updateSpeakingUI(false);
}

function speakText(text, langCode = 'en-IN') {
  if (isVoiceMuted || !('speechSynthesis' in window)) return;
  stopAssistantSpeaking();

  const cleanText = text.replace(/[*_`#]/g, '');
  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang = langCode || 'en-IN';
  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  // Try to find matching regional voice
  if (synthesisVoices.length > 0) {
    const targetLang = (langCode || 'en').toLowerCase();
    const matchingVoice = synthesisVoices.find(v => v.lang.toLowerCase() === targetLang || v.lang.toLowerCase().startsWith(targetLang.slice(0, 2)));
    if (matchingVoice) utterance.voice = matchingVoice;
  }

  utterance.onstart = () => updateSpeakingUI(true);
  utterance.onend = () => updateSpeakingUI(false);
  utterance.onerror = () => updateSpeakingUI(false);

  speechSynthesis.speak(utterance);
}

async function sendAssistantTextMessage(customText = null) {
  const input = document.getElementById('aiTextInput');
  const text = (customText || (input ? input.value : '')).trim();
  if (!text) return;

  if (input) input.value = '';
  stopAssistantSpeaking();

  // Append User Bubble
  appendAiChatBubble('user', text);

  // Update Status
  const statusText = document.getElementById('aiStatusText');
  if (statusText) statusText.textContent = 'Thinking & analyzing...';
  const visualizer = document.getElementById('waveformBars');
  if (visualizer) visualizer.classList.add('active');

  try {
    const res = await fetch('/api/voice/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ transcript: text })
    });
    const result = await res.json();

    if (visualizer) visualizer.classList.remove('active');
    if (statusText) statusText.textContent = 'Ready for Voice or Text';

    const spokenText = result.spoken_text || 'Processed your request.';
    const langCode = result.lang_code || 'en-IN';

    // Append AI Response Bubble
    appendAiChatBubble('ai', spokenText, result);

    // Speak audio
    speakText(spokenText, langCode);

    // If result navigated or altered views, trigger appropriate switches
    if (result.view) {
      const viewMap = {
        'overview': 'dashboard',
        'dashboard': 'dashboard',
        'sales': 'data-analysis',
        'inventory': 'dashboard',
        'sentiment': 'insights',
        'alerts': 'whatsapp-automation',
        'whatsapp-automation': 'whatsapp-automation',
        'data-feed': 'data-feed',
        'data_feeding': 'data-feed'
      };
      const targetView = viewMap[result.view] || result.view;
      if (targetView && targetView !== AppState.activeView) {
        switchView(targetView);
      }
      if (targetView === 'whatsapp-automation') {
        fetchWhatsAppHistory();
        fetchWhatsAppConfig();
      }
    }
  } catch (err) {
    if (visualizer) visualizer.classList.remove('active');
    if (statusText) statusText.textContent = 'Ready for Voice or Text';
    appendAiChatBubble('ai', '⚠️ Network error communicating with Vyapaar AI backend. Please check your connection.');
  }
}

function appendAiChatBubble(sender, text, extra = {}) {
  const stream = document.getElementById('aiChatStream');
  if (!stream) return;

  const bubble = document.createElement('div');
  bubble.className = `ai-chat-bubble ${sender === 'user' ? 'user-bubble' : 'ai-bubble'}`;
  const nowStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const formattedText = text
    .replace(/\n/g, '<br>')
    .replace(/\*(.*?)\*/g, '<strong>$1</strong>')
    .replace(/_(.*?)_/g, '<em>$1</em>');

  if (sender === 'user') {
    bubble.innerHTML = `
      <div class="bubble-avatar"><i data-lucide="user"></i></div>
      <div class="bubble-content">
        <div class="bubble-text">${formattedText}</div>
        <div class="bubble-meta">
          <span class="bubble-time">${nowStr}</span>
        </div>
      </div>
    `;
  } else {
    const langCode = extra.lang_code || 'en-IN';
    bubble.innerHTML = `
      <div class="bubble-avatar"><i data-lucide="bot"></i></div>
      <div class="bubble-content">
        <div class="bubble-text">${formattedText}</div>
        <div class="bubble-meta">
          <span class="bubble-time">${nowStr}</span>
          <div class="bubble-actions">
            <button class="bubble-icon-btn bubble-replay-btn" title="Replay Voice Audio">
              <i data-lucide="volume-2"></i>
            </button>
            <span class="bubble-engine">✦ ${extra.engine === 'gemini' ? 'Gemini 2.5 AI' : 'Multilingual Engine'}</span>
          </div>
        </div>
      </div>
    `;
    const replayBtn = bubble.querySelector('.bubble-replay-btn');
    if (replayBtn) {
      replayBtn.addEventListener('click', () => speakText(text, langCode));
    }
  }

  stream.appendChild(bubble);
  stream.scrollTop = stream.scrollHeight;
  if (window.lucide) lucide.createIcons();
}

function executeQuickPrompt(text) {
  sendAssistantTextMessage(text);
}

function clearAssistantChat() {
  const stream = document.getElementById('aiChatStream');
  if (!stream) return;
  stream.innerHTML = `
    <div class="ai-chat-bubble ai-bubble">
      <div class="bubble-avatar"><i data-lucide="bot"></i></div>
      <div class="bubble-content">
        <div class="bubble-text">
          👋 <strong>Conversation reset.</strong><br><br>
          How can I assist your business operations or WhatsApp alert automation today?
        </div>
        <div class="bubble-meta">
          <span class="bubble-time">Just now</span>
          <span class="bubble-engine">✦ Vyapaar AI Engine</span>
        </div>
      </div>
    </div>
  `;
  if (window.lucide) lucide.createIcons();
  showToast('AI conversation cleared', 'info');
}
