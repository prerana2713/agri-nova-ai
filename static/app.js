(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);

  const VIEW_META = {
    'overview': { title: 'Overview', crumb: 'WORKSPACE / OVERVIEW', i18nKey: 'nav_overview' },
    'soil-analysis': { title: 'Soil Analysis', crumb: 'WORKSPACE / SOIL ANALYSIS', i18nKey: 'nav_soil' },
    'crop-recommendation': { title: 'Crop Recommendation', crumb: 'WORKSPACE / CROP RECOMMENDATION', i18nKey: 'nav_crop' },
    'pest-camera': { title: 'Pest & Camera AI', crumb: 'WORKSPACE / PEST & CAMERA AI', i18nKey: 'nav_pest' },
    'farm-planner': { title: 'Farm Planner & Map', crumb: 'WORKSPACE / FARM PLANNER & MAP', i18nKey: 'nav_planner' },
    'fertilizer-guide': { title: 'Fertilizer Guide', crumb: 'WORKSPACE / FERTILIZER GUIDE', i18nKey: 'nav_guide' },
    'weather': { title: 'Weather', crumb: 'WORKSPACE / WEATHER', i18nKey: 'nav_weather' },
    'ai-assistant': { title: 'AI Assistant', crumb: 'WORKSPACE / AI ASSISTANT', i18nKey: 'nav_assistant' },
    'reports-history': { title: 'Reports History', crumb: 'WORKSPACE / REPORTS HISTORY', i18nKey: 'nav_history' },
    'settings': { title: 'Settings', crumb: 'WORKSPACE / SETTINGS', i18nKey: 'nav_settings' },
  };

  const I18N = {
    en: {
      nav_overview: 'Overview',
      nav_soil: 'Soil Analysis',
      nav_crop: 'Crop Recommendation',
      nav_pest: 'Pest & Camera AI',
      nav_planner: 'Farm Planner & Map',
      nav_guide: 'Fertilizer Guide',
      nav_weather: 'Weather',
      nav_assistant: 'AI Assistant',
      nav_history: 'Reports History',
      nav_settings: 'Settings',
      hero_title: 'Precision Agriculture. Smarter Decisions. Sustainable Farming.',
      hero_subtitle: 'Analyze soil nutrients with your Random Forest model, inspect NPK balance & ML feature importances, compare plots over time, monitor weather advisories, and export QR-stamped PDF reports.',
      cta_soil: 'Start Soil Analysis →',
      cta_crop: 'Crop Recommendation',
      cta_weather: 'Check Weather',
      kpi_total: 'Total Soil Analyses',
      kpi_score: 'Latest Soil Match Index',
      kpi_fert: 'Latest Fertilizer Prediction',
      kpi_reports: 'Reports Generated',
      sa_heading: 'Soil Nutrient & Fertilizer Analysis',
      lbl_crop: 'Crop Type',
      lbl_soil: 'Soil Type',
      lbl_temp: 'Temperature',
      lbl_humidity: 'Relative Humidity (%)',
      lbl_nitrogen: 'Nitrogen (N)',
      lbl_phosphorus: 'Phosphorus (P)',
      lbl_potassium: 'Potassium (K)',
      lbl_ph: 'Soil pH',
      lbl_moisture: 'Soil Moisture (%)',
      btn_analyze: 'Analyze Soil & Predict Fertilizer →',
    },
    hi: {
      nav_overview: 'डैशबोर्ड',
      nav_soil: 'मृदा विश्लेषण',
      nav_crop: 'फसल सुझाव',
      nav_pest: 'कीट और कैमरा AI',
      nav_planner: 'फार्म प्लानर और मानचित्र',
      nav_guide: 'उर्वरक मार्गदर्शिका',
      nav_weather: 'मौसम',
      nav_assistant: 'एआई सहायक',
      nav_history: 'रिपोर्ट इतिहास',
      nav_settings: 'सेटिंग्स',
      hero_title: 'सटीक कृषि। बेहतर निर्णय। टिकाऊ खेती।',
      hero_subtitle: 'अपने Random Forest मॉडल से मिट्टी के पोषक तत्वों का विश्लेषण करें, NPK संतुलन और फीचर महत्व देखें, मौसम सलाह जांचें और QR-सत्यापित PDF रिपोर्ट डाउनलोड करें।',
      cta_soil: 'मृदा विश्लेषण शुरू करें →',
      cta_crop: 'फसल सुझाव',
      cta_weather: 'मौसम देखें',
      kpi_total: 'कुल मृदा विश्लेषण',
      kpi_score: 'नवीनतम मृदा मिलान सूचकांक',
      kpi_fert: 'नवीनतम उर्वरक अनुमान',
      kpi_reports: 'बनाई गई रिपोर्ट',
      sa_heading: 'मृदा पोषक तत्व और उर्वरक विश्लेषण',
      lbl_crop: 'फसल का प्रकार',
      lbl_soil: 'मिट्टी का प्रकार',
      lbl_temp: 'तापमान',
      lbl_humidity: 'नमी (%)',
      lbl_nitrogen: 'नाइट्रोजन (N)',
      lbl_phosphorus: 'फॉस्फोरस (P)',
      lbl_potassium: 'पोटैशियम (K)',
      lbl_ph: 'मिट्टी का pH',
      lbl_moisture: 'मिट्टी की नमी (%)',
      btn_analyze: 'मिट्टी का विश्लेषण करें →',
    },
    kn: {
      nav_overview: 'ಅವಲೋಕನ',
      nav_soil: 'ಮಣ್ಣಿನ ವಿಶ್ಲೇಷಣೆ',
      nav_crop: 'ಬೆಳೆ ಸಲಹೆ',
      nav_pest: 'ಕೀಟ ಮತ್ತು ಕ್ಯಾಮೆರಾ AI',
      nav_planner: 'ಫಾರ್ಮ್ ಪ್ಲಾನರ್ ಮತ್ತು ನಕ್ಷೆ',
      nav_guide: 'ರಸಗೊಬ್ಬರ ಮಾರ್ಗದರ್ಶಿ',
      nav_weather: 'ಹವಾಮಾನ',
      nav_assistant: 'AI ಸಹಾಯಕ',
      nav_history: 'ವರದಿ ಇತಿಹಾಸ',
      nav_settings: 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು',
      hero_title: 'ನಿಖರ ಕೃಷಿ. ಸ್ಮಾರ್ಟ್ ನಿರ್ಧಾರಗಳು. ಸುಸ್ಥಿರ ಬೇಸಾಯ.',
      hero_subtitle: 'ನಿಮ್ಮ Random Forest ಮಾದರಿಯೊಂದಿಗೆ ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಿ, NPK ಸಮತೋಲನ ಮತ್ತು ಹವಾಮಾನ ಸಲಹೆಗಳನ್ನು ನೋಡಿ, ಹಾಗೂ QR-ಪ್ರಮಾಣಿತ PDF ವರದಿಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.',
      cta_soil: 'ಮಣ್ಣಿನ ವಿಶ್ಲೇಷಣೆ ಪ್ರಾರಂಭಿಸಿ →',
      cta_crop: 'ಬೆಳೆ ಸಲಹೆ',
      cta_weather: 'ಹವಾಮಾನ ನೋಡಿ',
      kpi_total: 'ಒಟ್ಟು ಮಣ್ಣಿನ ವಿಶ್ಲೇಷಣೆಗಳು',
      kpi_score: 'ಇತ್ತೀಚಿನ ಮಣ್ಣು ಹೊಂದಾಣಿಕೆ ಸೂಚ್ಯಂಕ',
      kpi_fert: 'ಇತ್ತೀಚಿನ ಗೊಬ್ಬರ ಮುನ್ಸೂಚನೆ',
      kpi_reports: 'ರಚಿಸಿದ ವರದಿಗಳು',
      sa_heading: 'ಮಣ್ಣಿನ ಪೋಷಕಾಂಶ ಮತ್ತು ಗೊಬ್ಬರ ವಿಶ್ಲೇಷಣೆ',
      lbl_crop: 'ಬೆಳೆ ಪ್ರಕಾರ',
      lbl_soil: 'ಮಣ್ಣಿನ ಪ್ರಕಾರ',
      lbl_temp: 'ತಾಪಮಾನ',
      lbl_humidity: 'ಆರ್ದ್ರತೆ (%)',
      lbl_nitrogen: 'ನೈಟ್ರೋಜನ್ (N)',
      lbl_phosphorus: 'ಫಾಸ್ಫರಸ್ (P)',
      lbl_potassium: 'ಪೊಟ್ಯಾಸಿಯಮ್ (K)',
      lbl_ph: 'ಮಣ್ಣಿನ pH',
      lbl_moisture: 'ಮಣ್ಣಿನ ತೇವಾಂಶ (%)',
      btn_analyze: 'ಮಣ್ಣು ವಿಶ್ಲೇಷಿಸಿ →',
    },
  };

  const state = {
    activeView: 'overview',
    user: null,
    lang: localStorage.getItem('agri_nova_lang') || 'en',
    theme: localStorage.getItem('agri_nova_theme') || 'light',
    units: localStorage.getItem('agri_nova_units') || 'metric',
    latestAnalysis: null,
    latestInputs: null,
    plots: [],
    guideItems: [],
    compareIds: [],
    compareReportIds: [],
    batchResults: [],
    weatherData: null,
    weatherLoaded: false,
    modelInsightsLoaded: false,
    chatMessages: [
      {
        role: 'bot',
        text: 'Hello! I am the Agri Nova AI Assistant (local rule-based engine). Ask me about your latest soil analysis, NPK nutrients, fertilizers, pH, or crops.',
      },
    ],
    charts: {
      overviewNpk: null,
      overviewTrend: null,
      soilRadar: null,
    },
    confirmCallback: null,
    simTimer: null,
  };

  // ==========================================
  // UTILITIES & I18N
  // ==========================================

  function showToast(message, type = 'info') {
    const container = $('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3600);
  }

  function formatTemp(tempC) {
    if (tempC === null || tempC === undefined || Number.isNaN(Number(tempC))) return 'N/A';
    const c = Number(tempC);
    if (state.units === 'imperial') {
      return `${((c * 9) / 5 + 32).toFixed(1)} °F`;
    }
    return `${c.toFixed(1)} °C`;
  }

  function applyLanguage(lang) {
    if (!I18N[lang]) lang = 'en';
    state.lang = lang;
    localStorage.setItem('agri_nova_lang', lang);
    const dict = I18N[lang];
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.dataset.i18n;
      if (dict[key]) el.textContent = dict[key];
    });
    if ($('lang-select')) $('lang-select').value = lang;
    if ($('pref-lang')) $('pref-lang').value = lang;
    const meta = VIEW_META[state.activeView];
    if (meta && dict[meta.i18nKey]) {
      $('topbar-title').textContent = dict[meta.i18nKey];
    }
  }

  function applyThemeAndUnits() {
    document.documentElement.setAttribute('data-theme', state.theme);
    const unitLabel = state.units === 'imperial' ? '°F' : '°C';
    document.querySelectorAll('.temp-unit-label').forEach((el) => {
      el.textContent = unitLabel;
    });
    if ($('pref-theme')) $('pref-theme').value = state.theme;
    if ($('pref-units')) $('pref-units').value = state.units;
    if (state.weatherData) renderWeatherData(state.weatherData);
  }

  async function apiFetch(url, options = {}) {
    const isFormData = options.body instanceof FormData;
    const headers = isFormData
      ? { ...(options.headers || {}) }
      : { 'Content-Type': 'application/json', ...(options.headers || {}) };
    const response = await fetch(url, { ...options, headers });
    let data = null;
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      data = await response.json();
    }
    if (!response.ok) {
      throw new Error((data && data.error) || `Request failed (${response.status})`);
    }
    return data;
  }

  function triggerBlobDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function openConfirmModal(title, message, onConfirm) {
    $('confirm-title').textContent = title;
    $('confirm-message').textContent = message;
    state.confirmCallback = onConfirm;
    $('confirm-modal').hidden = false;
  }

  function closeConfirmModal() {
    $('confirm-modal').hidden = true;
    state.confirmCallback = null;
  }

  // ==========================================
  // NAVIGATION
  // ==========================================

  function navigateTo(viewId) {
    if (!VIEW_META[viewId]) viewId = 'overview';
    state.activeView = viewId;

    document.querySelectorAll('.view-section').forEach((sec) => {
      sec.hidden = sec.id !== `view-${viewId}`;
      sec.classList.toggle('active', sec.id === `view-${viewId}`);
    });

    document.querySelectorAll('.nav-item').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.nav === viewId);
    });

    const dict = I18N[state.lang] || I18N.en;
    const meta = VIEW_META[viewId];
    $('topbar-title').textContent = dict[meta.i18nKey] || meta.title;
    $('topbar-crumb').textContent = meta.crumb;

    closeMobileNav();

    if (viewId === 'overview') loadDashboard();
    if (viewId === 'pest-camera') {
      loadPestScans();
      loadPestGuide();
    }
    if (viewId === 'farm-planner') {
      renderFarmMap();
      loadTasks();
      updateCalculators();
    }
    if (viewId === 'fertilizer-guide' && !state.guideItems.length) loadFertilizerGuide();
    if (viewId === 'weather' && !state.weatherLoaded) loadWeather($('weather-city-input').value || 'Bengaluru');
    if (viewId === 'reports-history') loadHistoryTable();
  }

  function closeMobileNav() {
    document.body.classList.remove('mobile-nav-open');
    if ($('mobile-backdrop')) $('mobile-backdrop').hidden = true;
  }

  function setupNavigation() {
    document.querySelectorAll('[data-nav], [data-nav-trigger]').forEach((el) => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const target = el.dataset.nav || el.dataset.navTrigger;
        if (target) navigateTo(target);
      });
    });

    $('sidebar-collapse-btn')?.addEventListener('click', () => {
      document.body.classList.toggle('sidebar-collapsed');
    });

    $('mobile-menu-btn')?.addEventListener('click', () => {
      document.body.classList.add('mobile-nav-open');
      $('mobile-backdrop').hidden = false;
    });

    $('mobile-backdrop')?.addEventListener('click', closeMobileNav);

    document.querySelectorAll('.seg-tabs').forEach((bar) => {
      const group = bar.dataset.tabGroup;
      bar.addEventListener('click', (e) => {
        const btn = e.target.closest('.seg-tab');
        if (!btn) return;
        const targetId = btn.dataset.tabTarget;
        bar.querySelectorAll('.seg-tab').forEach((t) => t.classList.toggle('active', t === btn));
        document.querySelectorAll(`.tab-pane[data-pane-group="${group}"]`).forEach((pane) => {
          const isMatch = pane.id === targetId;
          pane.hidden = !isMatch;
          pane.classList.toggle('active', isMatch);
        });
      });
    });
  }

  // ==========================================
  // AUTH & SETTINGS
  // ==========================================

  function updateAuthUI() {
    const user = state.user;
    if (user) {
      const display = user.full_name || user.username;
      $('sidebar-user-name').textContent = display;
      $('sidebar-user-sub').textContent = user.farm_location || `@${user.username}`;
      $('sidebar-avatar').textContent = display.slice(0, 2).toUpperCase();
      $('sidebar-auth-btn').textContent = 'Account';
      $('topbar-auth-btn').textContent = `Signed in: ${user.username}`;

      $('settings-guest-box').hidden = true;
      $('settings-profile-form').hidden = false;
      $('prof-username').value = user.username || '';
      $('prof-email').value = user.email || '';
      $('prof-fullname').value = user.full_name || '';
      $('prof-location').value = user.farm_location || '';

      if (user.preferred_theme) {
        state.theme = user.preferred_theme;
        localStorage.setItem('agri_nova_theme', state.theme);
      }
      if (user.preferred_units) {
        state.units = user.preferred_units;
        localStorage.setItem('agri_nova_units', state.units);
      }
      applyThemeAndUnits();
    } else {
      $('sidebar-user-name').textContent = 'Guest Workspace';
      $('sidebar-user-sub').textContent = 'Academic Demo Mode';
      $('sidebar-avatar').textContent = 'GN';
      $('sidebar-auth-btn').textContent = 'Sign In';
      $('topbar-auth-btn').textContent = 'Sign In / Register';

      $('settings-guest-box').hidden = false;
      $('settings-profile-form').hidden = true;
    }
  }

  function openAuthModal(tab = 'login') {
    $('auth-modal').hidden = false;
    switchAuthTab(tab);
  }

  function switchAuthTab(tab) {
    const isLogin = tab === 'login';
    $('tab-login').classList.toggle('active', isLogin);
    $('tab-register').classList.toggle('active', !isLogin);
    $('login-form').hidden = !isLogin;
    $('register-form').hidden = isLogin;
    $('auth-modal-title').textContent = isLogin ? 'Sign In' : 'Create Account';
    $('login-error').hidden = true;
    $('register-error').hidden = true;
  }

  async function refreshSession() {
    try {
      const data = await apiFetch('/api/auth/me');
      state.user = data.authenticated ? data.user : null;
      updateAuthUI();
    } catch {
      state.user = null;
      updateAuthUI();
    }
  }

  function setupAuthAndSettings() {
    $('lang-select')?.addEventListener('change', (e) => applyLanguage(e.target.value));
    $('pref-lang')?.addEventListener('change', (e) => {
      applyLanguage(e.target.value);
      showToast('Language updated.', 'success');
    });

    $('topbar-auth-btn')?.addEventListener('click', () => {
      if (state.user) navigateTo('settings');
      else openAuthModal('login');
    });
    $('sidebar-auth-btn')?.addEventListener('click', () => {
      if (state.user) navigateTo('settings');
      else openAuthModal('login');
    });
    $('settings-open-login')?.addEventListener('click', () => openAuthModal('login'));
    $('settings-open-register')?.addEventListener('click', () => openAuthModal('register'));
    $('auth-close')?.addEventListener('click', () => ($('auth-modal').hidden = true));
    $('tab-login')?.addEventListener('click', () => switchAuthTab('login'));
    $('tab-register')?.addEventListener('click', () => switchAuthTab('register'));

    $('login-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      $('login-error').hidden = true;
      try {
        const res = await apiFetch('/api/auth/login', {
          method: 'POST',
          body: JSON.stringify({
            identifier: $('login-identifier').value.trim(),
            password: $('login-password').value,
          }),
        });
        state.user = res.user;
        updateAuthUI();
        $('auth-modal').hidden = true;
        showToast(`Welcome back, ${res.user.full_name || res.user.username}!`, 'success');
        await loadPlots();
        await loadDashboard();
        if (state.activeView === 'reports-history') loadHistoryTable();
      } catch (err) {
        $('login-error').textContent = err.message;
        $('login-error').hidden = false;
      }
    });

    $('register-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      $('register-error').hidden = true;
      try {
        const res = await apiFetch('/api/auth/register', {
          method: 'POST',
          body: JSON.stringify({
            username: $('reg-username').value.trim(),
            email: $('reg-email').value.trim(),
            full_name: $('reg-fullname').value.trim(),
            password: $('reg-password').value,
          }),
        });
        state.user = res.user;
        updateAuthUI();
        $('auth-modal').hidden = true;
        showToast('Account created and signed in.', 'success');
        await loadPlots();
        await loadDashboard();
      } catch (err) {
        $('register-error').textContent = err.message;
        $('register-error').hidden = false;
      }
    });

    $('settings-logout-btn')?.addEventListener('click', async () => {
      await apiFetch('/api/auth/logout', { method: 'POST' });
      state.user = null;
      updateAuthUI();
      showToast('Signed out to Guest Workspace.', 'info');
      await loadPlots();
      await loadDashboard();
    });

    $('settings-profile-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const res = await apiFetch('/api/auth/profile', {
          method: 'PUT',
          body: JSON.stringify({
            full_name: $('prof-fullname').value.trim(),
            farm_location: $('prof-location').value.trim(),
            preferred_theme: state.theme,
            preferred_units: state.units,
          }),
        });
        state.user = res.user;
        updateAuthUI();
        showToast('Profile saved.', 'success');
      } catch (err) {
        showToast(err.message, 'error');
      }
    });

    $('pref-theme')?.addEventListener('change', async (e) => {
      state.theme = e.target.value;
      localStorage.setItem('agri_nova_theme', state.theme);
      applyThemeAndUnits();
      if (state.user) {
        await apiFetch('/api/auth/profile', {
          method: 'PUT',
          body: JSON.stringify({ preferred_theme: state.theme }),
        }).catch(() => {});
      }
      showToast('Theme preference updated.', 'success');
    });

    $('pref-units')?.addEventListener('change', async (e) => {
      state.units = e.target.value;
      localStorage.setItem('agri_nova_units', state.units);
      applyThemeAndUnits();
      if (state.user) {
        await apiFetch('/api/auth/profile', {
          method: 'PUT',
          body: JSON.stringify({ preferred_units: state.units }),
        }).catch(() => {});
      }
      showToast('Temperature unit updated.', 'success');
    });

    $('settings-manage-plots')?.addEventListener('click', openPlotsModal);
    $('settings-export-csv')?.addEventListener('click', exportReportsCSV);
    $('settings-clear-history')?.addEventListener('click', confirmClearHistory);
  }

  // ==========================================
  // FIELD PLOTS MANAGEMENT
  // ==========================================

  async function loadPlots() {
    try {
      const data = await apiFetch('/api/plots');
      state.plots = data.plots || [];
      syncPlotSelectors();
      renderPlotsList();
      if (state.activeView === 'farm-planner') renderFarmMap();
    } catch {
      state.plots = [];
    }
  }

  function syncPlotSelectors() {
    const selectors = [
      { el: $('sa-plot-id'), emptyLabel: 'No specific plot (General workspace)' },
      { el: $('batch-plot-id'), emptyLabel: 'No specific plot' },
      { el: $('task-plot-id'), emptyLabel: 'General Workspace' },
      { el: $('rh-plot-filter'), emptyLabel: 'All Field Plots', emptyVal: 'all' },
    ];
    selectors.forEach(({ el, emptyLabel, emptyVal = '' }) => {
      if (!el) return;
      const prev = el.value;
      el.replaceChildren();
      const defOpt = document.createElement('option');
      defOpt.value = emptyVal;
      defOpt.textContent = emptyLabel;
      el.appendChild(defOpt);
      state.plots.forEach((p) => {
        const opt = document.createElement('option');
        opt.value = String(p.id);
        opt.textContent = `${p.name} (${p.soil_type})`;
        el.appendChild(opt);
      });
      if ([...el.options].some((o) => o.value === prev)) el.value = prev;
    });
  }

  function renderPlotsList() {
    const wrap = $('plots-list-wrap');
    if (!wrap) return;
    wrap.replaceChildren();
    if (!state.plots.length) {
      const p = document.createElement('p');
      p.className = 'muted-text';
      p.textContent = 'No field plots added yet. Create one above to organize analyses by field.';
      wrap.appendChild(p);
      return;
    }
    state.plots.forEach((plot) => {
      const row = document.createElement('div');
      row.className = 'recent-row';
      const left = document.createElement('div');
      const strong = document.createElement('strong');
      strong.textContent = `${plot.name} (${plot.soil_type})`;
      const small = document.createElement('small');
      small.textContent = `${plot.location || 'Location not set'} · ${plot.area_acres ? `${plot.area_acres} acres · ` : ''}${plot.report_count || 0} reports`;
      left.append(strong, small);

      const del = document.createElement('button');
      del.type = 'button';
      del.className = 'btn-danger-outline btn-xs';
      del.textContent = 'Remove';
      del.addEventListener('click', async () => {
        await apiFetch(`/api/plots/${plot.id}`, { method: 'DELETE' });
        showToast('Plot removed.', 'info');
        await loadPlots();
        await loadDashboard();
      });
      row.append(left, del);
      wrap.appendChild(row);
    });
  }

  function openPlotsModal() {
    loadPlots();
    $('plots-modal').hidden = false;
  }

  function setupPlotsModal() {
    $('open-plots-modal-btn')?.addEventListener('click', openPlotsModal);
    $('rh-manage-plots-btn')?.addEventListener('click', openPlotsModal);
    $('fp-manage-plots-btn')?.addEventListener('click', openPlotsModal);
    $('plots-close')?.addEventListener('click', () => ($('plots-modal').hidden = true));
    $('plots-close-btn')?.addEventListener('click', () => ($('plots-modal').hidden = true));

    $('sa-plot-id')?.addEventListener('change', (e) => {
      const plot = state.plots.find((p) => String(p.id) === e.target.value);
      if (plot && $('sa-soil-type')) {
        $('sa-soil-type').value = plot.soil_type;
        showToast(`Auto-selected ${plot.soil_type} soil for ${plot.name}.`, 'info');
      }
    });

    $('plot-create-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        await apiFetch('/api/plots', {
          method: 'POST',
          body: JSON.stringify({
            name: $('plot-name-input').value.trim(),
            soil_type: $('plot-soil-input').value,
            location: $('plot-location-input').value.trim(),
            area_acres: $('plot-area-input').value,
            latitude: $('plot-lat-input')?.value || '',
            longitude: $('plot-lon-input')?.value || '',
          }),
        });
        $('plot-create-form').reset();
        showToast('Field plot added.', 'success');
        await loadPlots();
        await loadDashboard();
      } catch (err) {
        showToast(err.message, 'error');
      }
    });
  }

  // ==========================================
  // CHARTS & MODEL INSIGHTS
  // ==========================================

  function renderNpkBars(container, gaps) {
    container.replaceChildren();
    (gaps || []).forEach((item) => {
      const wrapper = document.createElement('div');
      wrapper.className = 'bar-item';

      const heading = document.createElement('div');
      heading.className = 'bar-heading';

      const left = document.createElement('div');
      left.className = 'bar-left';

      const title = document.createElement('strong');
      title.textContent = item.name;

      const status = document.createElement('span');
      const norm = String(item.status || '').toLowerCase();
      status.className = `status-tag ${norm.includes('low') ? 'status-low' : norm.includes('high') ? 'status-high' : 'status-normal'}`;
      status.textContent = item.status;
      left.append(title, status);

      const pctText = document.createElement('strong');
      pctText.textContent = `${item.percent}%`;
      heading.append(left, pctText);

      const track = document.createElement('div');
      track.className = 'bar-track';

      const fill = document.createElement('div');
      fill.className = `bar-fill ${norm.includes('low') ? 'fill-low' : norm.includes('high') ? 'fill-high' : 'fill-normal'}`;
      fill.style.width = `${Math.max(0, Math.min(100, Number(item.percent) || 0))}%`;
      track.appendChild(fill);

      wrapper.append(heading, track);
      container.appendChild(wrapper);
    });
  }

  function renderTreeVotes(container, votes) {
    container.replaceChildren();
    if (!votes || !votes.length) {
      const p = document.createElement('p');
      p.className = 'muted-text';
      p.textContent = 'Tree-vote split unavailable for legacy record.';
      container.appendChild(p);
      return;
    }
    votes.forEach((v) => {
      const wrapper = document.createElement('div');
      wrapper.className = 'bar-item';
      const head = document.createElement('div');
      head.className = 'bar-heading';
      const name = document.createElement('strong');
      name.textContent = v.fertilizer;
      const pct = document.createElement('strong');
      pct.textContent = `${v.tree_share_pct}% tree votes`;
      head.append(name, pct);

      const track = document.createElement('div');
      track.className = 'bar-track';
      const fill = document.createElement('div');
      fill.className = 'bar-fill fill-normal';
      fill.style.width = `${Math.max(2, Math.min(100, Number(v.tree_share_pct) || 0))}%`;
      track.appendChild(fill);
      wrapper.append(head, track);
      container.appendChild(wrapper);
    });
  }

  function renderSvgRadar(container, gaps) {
    if (!container || !Array.isArray(gaps) || gaps.length !== 3) return;
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 340 280');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'NPK radar chart');

    const cx = 170;
    const cy = 135;
    const radius = 84;
    const angles = [-90, 30, 150];

    [25, 50, 75, 100].forEach((lvl) => {
      const pts = angles.map((a) => {
        const rad = (a * Math.PI) / 180;
        const r = (radius * lvl) / 100;
        return `${cx + Math.cos(rad) * r},${cy + Math.sin(rad) * r}`;
      }).join(' ');
      const poly = document.createElementNS(ns, 'polygon');
      poly.setAttribute('points', pts);
      poly.setAttribute('fill', 'none');
      poly.setAttribute('stroke', '#DCE6DE');
      svg.appendChild(poly);
    });

    const points = gaps.map((g, i) => {
      const rad = (angles[i] * Math.PI) / 180;
      const val = Math.max(0, Math.min(100, Number(g.percent) || 0));
      return {
        x: cx + (Math.cos(rad) * radius * val) / 100,
        y: cy + (Math.sin(rad) * radius * val) / 100,
        ax: cx + Math.cos(rad) * radius,
        ay: cy + Math.sin(rad) * radius,
        label: `${g.name} (${val}%)`,
      };
    });

    points.forEach((p) => {
      const line = document.createElementNS(ns, 'line');
      line.setAttribute('x1', cx);
      line.setAttribute('y1', cy);
      line.setAttribute('x2', p.ax);
      line.setAttribute('y2', p.ay);
      line.setAttribute('stroke', '#C0D2C4');
      svg.appendChild(line);
    });

    const area = document.createElementNS(ns, 'polygon');
    area.setAttribute('points', points.map((p) => `${p.x},${p.y}`).join(' '));
    area.setAttribute('fill', '#247A49');
    area.setAttribute('fill-opacity', '0.26');
    area.setAttribute('stroke', '#247A49');
    area.setAttribute('stroke-width', '2.5');
    svg.appendChild(area);

    points.forEach((p) => {
      const dot = document.createElementNS(ns, 'circle');
      dot.setAttribute('cx', p.x);
      dot.setAttribute('cy', p.y);
      dot.setAttribute('r', '5');
      dot.setAttribute('fill', '#123B26');
      dot.setAttribute('stroke', '#FFFFFF');
      dot.setAttribute('stroke-width', '2');
      svg.appendChild(dot);

      const txt = document.createElementNS(ns, 'text');
      txt.setAttribute('x', cx + (p.ax - cx) * 1.32);
      txt.setAttribute('y', cy + (p.ay - cy) * 1.32 + 4);
      txt.setAttribute('text-anchor', 'middle');
      txt.setAttribute('font-size', '11');
      txt.setAttribute('font-weight', '700');
      txt.setAttribute('fill', '#26352B');
      txt.textContent = p.label;
      svg.appendChild(txt);
    });

    container.replaceChildren(svg);
  }

  function renderSoilRadarChart(gaps) {
    const canvas = $('soilRadarChart');
    const fallback = $('soilRadarFallback');
    if (!gaps || gaps.length !== 3) {
      if (canvas) canvas.hidden = true;
      if (fallback) {
        fallback.hidden = false;
        fallback.textContent = 'NPK breakdown unavailable for legacy records without nutrient inputs.';
      }
      return;
    }

    if (typeof window.Chart === 'function' && canvas) {
      canvas.hidden = false;
      fallback.hidden = true;
      if (state.charts.soilRadar) state.charts.soilRadar.destroy();
      state.charts.soilRadar = new window.Chart(canvas, {
        type: 'radar',
        data: {
          labels: gaps.map((g) => g.name),
          datasets: [{
            label: 'Prototype Baseline Match (%)',
            data: gaps.map((g) => g.percent),
            backgroundColor: 'rgba(36, 122, 73, 0.22)',
            borderColor: '#247A49',
            pointBackgroundColor: '#123B26',
            borderWidth: 2,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: { r: { min: 0, max: 100, ticks: { stepSize: 25 } } },
        },
      });
    } else {
      if (canvas) canvas.hidden = true;
      if (fallback) {
        fallback.hidden = false;
        renderSvgRadar(fallback, gaps);
      }
    }
  }

  function renderOverviewNpkChart(latest) {
    const canvas = $('overviewNpkChart');
    const fallback = $('overviewNpkFallback');
    if (!latest || !Array.isArray(latest.gaps) || !latest.gaps.length) {
      if (canvas) canvas.hidden = true;
      if (fallback) {
        fallback.hidden = false;
        fallback.textContent = 'Run a new Soil Analysis to visualize N, P, and K levels.';
      }
      return;
    }

    if (typeof window.Chart === 'function' && canvas) {
      canvas.hidden = false;
      fallback.hidden = true;
      if (state.charts.overviewNpk) state.charts.overviewNpk.destroy();
      state.charts.overviewNpk = new window.Chart(canvas, {
        type: 'bar',
        data: {
          labels: latest.gaps.map((g) => g.name),
          datasets: [
            {
              label: 'Entered Value (kg/ha*)',
              data: latest.gaps.map((g) => g.value ?? 0),
              backgroundColor: '#247A49',
              borderRadius: 6,
            },
            {
              label: 'Illustrative Crop Baseline',
              data: latest.gaps.map((g) => g.target ?? 0),
              backgroundColor: '#B7DCC4',
              borderRadius: 6,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom' } },
          scales: { y: { beginAtZero: true } },
        },
      });
    } else {
      if (canvas) canvas.hidden = true;
      if (fallback) {
        fallback.hidden = false;
        renderNpkBars(fallback, latest.gaps);
      }
    }
  }

  function renderOverviewTrendChart(series) {
    const canvas = $('overviewTrendChart');
    const fallback = $('overviewTrendFallback');
    if (!series || !series.length) {
      if (canvas) canvas.hidden = true;
      if (fallback) {
        fallback.hidden = false;
        fallback.textContent = 'Complete soil analyses to see historical Match Index trends.';
      }
      return;
    }

    if (typeof window.Chart === 'function' && canvas) {
      canvas.hidden = false;
      fallback.hidden = true;
      if (state.charts.overviewTrend) state.charts.overviewTrend.destroy();
      state.charts.overviewTrend = new window.Chart(canvas, {
        type: 'line',
        data: {
          labels: series.map((s) => s.label),
          datasets: [{
            label: 'Demo Soil Match Index (/100)',
            data: series.map((s) => s.score),
            borderColor: '#247A49',
            backgroundColor: 'rgba(36, 122, 73, 0.14)',
            fill: true,
            tension: 0.3,
            pointBackgroundColor: '#123B26',
            pointRadius: 4,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom' } },
          scales: { y: { min: 0, max: 100 } },
        },
      });
    } else {
      if (canvas) canvas.hidden = true;
      if (fallback) {
        fallback.hidden = false;
        fallback.textContent = `Latest Match Indices: ${series.map((s) => `${s.crop}: ${s.score}`).join(' · ')}`;
      }
    }
  }

  async function loadModelInsights() {
    if (state.modelInsightsLoaded) return;
    try {
      const data = await apiFetch('/api/model-insights');
      state.modelInsightsLoaded = true;
      $('model-trees-badge').textContent = `${data.n_estimators} Trees · ${data.dataset?.rows || 99} Rows`;
      $('model-transparency-note').textContent = data.transparency_note || '';

      const wrap = $('model-importance-bars');
      wrap.replaceChildren();
      (data.feature_importances || []).forEach((feat) => {
        const item = document.createElement('div');
        item.className = 'bar-item';
        const head = document.createElement('div');
        head.className = 'bar-heading';
        const name = document.createElement('strong');
        name.textContent = feat.feature;
        const val = document.createElement('strong');
        val.textContent = `${feat.importance_pct}%`;
        head.append(name, val);

        const track = document.createElement('div');
        track.className = 'bar-track';
        const fill = document.createElement('div');
        fill.className = 'bar-fill fill-normal';
        fill.style.width = `${Math.max(2, Math.min(100, feat.importance_pct * 2.2))}%`;
        track.appendChild(fill);
        item.append(head, track);
        wrap.appendChild(item);
      });
    } catch {
      // Non-fatal
    }
  }

  // ==========================================
  // DASHBOARD OVERVIEW
  // ==========================================

  async function loadDashboard() {
    try {
      loadModelInsights();
      const data = await apiFetch('/api/dashboard');
      $('current-date-chip').textContent = data.server_date || new Date().toDateString();
      $('kpi-total').textContent = data.total_analyses;
      $('kpi-reports').textContent = data.reports_generated;
      $('kpi-plots-sub').textContent = `${data.plots_count || 0} saved field plot(s)`;

      const latest = data.latest_analysis;
      if (latest) {
        $('kpi-score').textContent = `${latest.score}/100`;
        $('kpi-score-sub').textContent = `${latest.crop} (${latest.soil_type || 'Soil'})`;
        $('kpi-fert').textContent = latest.fertilizer || 'Not recorded';
        $('kpi-fert-sub').textContent = latest.date || 'Latest saved record';
        $('overview-latest-crop').textContent = `${latest.crop} · ${latest.fertilizer}`;

        if (!state.latestAnalysis && latest.gaps && latest.gaps.length) {
          state.latestAnalysis = latest;
          state.latestInputs = {
            crop: latest.crop,
            soil_type: latest.soil_type,
            temperature: latest.temperature,
            humidity: latest.humidity,
            moisture: latest.moisture,
            nitrogen: latest.nitrogen,
            phosphorus: latest.phosphorus,
            potassium: latest.potassium,
            ph: latest.ph,
          };
        }
      } else {
        $('kpi-score').textContent = '—';
        $('kpi-score-sub').textContent = 'Awaiting first analysis';
        $('kpi-fert').textContent = '—';
        $('kpi-fert-sub').textContent = 'Random Forest output';
      }

      const hasData = data.total_analyses > 0;
      $('overview-empty').hidden = hasData;
      $('overview-data-grid').hidden = !hasData;

      if (hasData) {
        renderOverviewNpkChart(latest);
        renderOverviewTrendChart(data.trend_series || []);
        renderHealthSummaryCard(latest);
      }

      const recentWrap = $('overview-recent-list');
      recentWrap.replaceChildren();
      if (!data.recent_history || !data.recent_history.length) {
        const emptyP = document.createElement('p');
        emptyP.className = 'muted-text';
        emptyP.textContent = 'No recent soil analyses yet.';
        recentWrap.appendChild(emptyP);
      } else {
        data.recent_history.forEach((item) => {
          const row = document.createElement('div');
          row.className = 'recent-row';
          const left = document.createElement('div');
          const title = document.createElement('strong');
          title.textContent = `${item.crop} — ${item.fertilizer}`;
          const sub = document.createElement('small');
          sub.textContent = `${item.date}${item.plot_name ? ` · ${item.plot_name}` : ''} · Match ${item.score}/100`;
          left.append(title, sub);

          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'btn-outline btn-xs';
          btn.textContent = 'Inspect';
          btn.addEventListener('click', () => openReportDetailModal(item.id));
          row.append(left, btn);
          recentWrap.appendChild(row);
        });
      }

      const tipsWrap = $('overview-tips-list');
      tipsWrap.replaceChildren();
      (data.tips || []).forEach((tip) => {
        const div = document.createElement('div');
        div.className = 'tip-row';
        const strong = document.createElement('strong');
        strong.textContent = tip.title;
        const p = document.createElement('p');
        p.textContent = tip.detail;
        div.append(strong, p);
        tipsWrap.appendChild(div);
      });
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  function renderHealthSummaryCard(latest) {
    const box = $('overview-health-summary');
    box.replaceChildren();
    if (!latest || !latest.health || !latest.health.overall) {
      const p = document.createElement('p');
      p.className = 'muted-text';
      p.textContent = latest
        ? `Latest record: ${latest.crop} (${latest.fertilizer}), Match Index ${latest.score}/100. Run a full analysis for detailed NPK observations.`
        : 'No analysis loaded.';
      box.appendChild(p);
      return;
    }

    const head = document.createElement('div');
    head.className = 'alert-info';
    head.textContent = `${latest.health.overall}: ${latest.health.note}`;
    box.appendChild(head);

    (latest.health.observations || []).slice(0, 3).forEach((obs) => {
      const item = document.createElement('div');
      item.className = 'obs-item';
      const h = document.createElement('div');
      h.className = 'obs-item-head';
      const t = document.createElement('strong');
      t.textContent = obs.title;
      const s = document.createElement('span');
      s.className = 'badge-pill';
      s.textContent = obs.status;
      h.append(t, s);
      const p = document.createElement('p');
      p.textContent = obs.detail;
      item.append(h, p);
      box.appendChild(item);
    });
  }

  // ==========================================
  // SOIL ANALYSIS + SIMULATOR + BATCH CSV
  // ==========================================

  function setSoilMode(mode) {
    $('sa-single-pane').hidden = mode !== 'single';
    $('sa-batch-pane').hidden = mode !== 'batch';
    $('sa-iot-pane').hidden = mode !== 'iot';
    $('sa-mode-single-btn').className = mode === 'single' ? 'btn-primary btn-sm' : 'btn-outline btn-sm';
    $('sa-mode-batch-btn').className = mode === 'batch' ? 'btn-primary btn-sm' : 'btn-outline btn-sm';
    $('sa-mode-iot-btn').className = mode === 'iot' ? 'btn-primary btn-sm' : 'btn-outline btn-sm';
    if (mode === 'iot') loadLatestIot();
  }

  function setupSoilAnalysis() {
    $('sa-mode-single-btn')?.addEventListener('click', () => setSoilMode('single'));
    $('sa-mode-batch-btn')?.addEventListener('click', () => setSoilMode('batch'));
    $('sa-mode-iot-btn')?.addEventListener('click', () => setSoilMode('iot'));

    const form = $('soil-form');
    if (form) {
      $('soil-sample-btn')?.addEventListener('click', () => {
        $('sa-crop').value = 'Wheat';
        $('sa-soil-type').value = 'Loamy';
        $('sa-temperature').value = state.units === 'imperial' ? '78.8' : '26';
        $('sa-humidity').value = '58';
        $('sa-nitrogen').value = '24';
        $('sa-phosphorus').value = '48';
        $('sa-potassium').value = '38';
        $('sa-ph').value = '6.6';
        $('sa-moisture').value = '46';
        showToast('Demo soil sample values loaded.', 'info');
      });

      $('soil-reset-btn')?.addEventListener('click', () => {
        form.reset();
        $('soil-form-error').hidden = true;
        $('sa-empty').hidden = false;
        $('sa-result').hidden = true;
        $('sa-status-badge').textContent = 'AWAITING INPUT';
      });

      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        $('soil-form-error').hidden = true;

        const payload = {
          plot_id: $('sa-plot-id')?.value || '',
          crop: $('sa-crop').value,
          soil_type: $('sa-soil-type').value,
          temperature: $('sa-temperature').value,
          humidity: $('sa-humidity').value,
          nitrogen: $('sa-nitrogen').value,
          phosphorus: $('sa-phosphorus').value,
          potassium: $('sa-potassium').value,
          ph: $('sa-ph').value,
          moisture: $('sa-moisture').value,
          temp_unit: state.units === 'imperial' ? 'F' : 'C',
        };

        const btn = $('soil-submit-btn');
        btn.disabled = true;
        btn.textContent = 'Analyzing Soil Sample...';

        try {
          const result = await apiFetch('/api/analyze', {
            method: 'POST',
            body: JSON.stringify(payload),
          });
          state.latestInputs = result.inputs;
          state.latestAnalysis = result;

          renderSoilResult(result);
          showToast(`Analysis complete: ${result.fertilizer} predicted.`, 'success');
          loadDashboard();
        } catch (err) {
          $('soil-form-error').textContent = err.message;
          $('soil-form-error').hidden = false;
          showToast(err.message, 'error');
        } finally {
          btn.disabled = false;
          applyLanguage(state.lang);
        }
      });
    }

    // What-If Simulator Sliders
    ['sim-n', 'sim-p', 'sim-k', 'sim-ph'].forEach((sliderId) => {
      $(sliderId)?.addEventListener('input', () => {
        $('sim-n-val').textContent = $('sim-n').value;
        $('sim-p-val').textContent = $('sim-p').value;
        $('sim-k-val').textContent = $('sim-k').value;
        $('sim-ph-val').textContent = $('sim-ph').value;
        clearTimeout(state.simTimer);
        state.simTimer = setTimeout(runWhatIfSimulation, 160);
      });
    });

    // Batch CSV Upload
    $('batch-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      $('batch-error').hidden = true;
      const fileInput = $('batch-file-input');
      if (!fileInput?.files?.length) {
        $('batch-error').textContent = 'Select a CSV file first.';
        $('batch-error').hidden = false;
        return;
      }

      const fd = new FormData();
      fd.append('file', fileInput.files[0]);
      fd.append('plot_id', $('batch-plot-id')?.value || '');
      fd.append('save_to_history', $('batch-save-cb')?.checked ? 'true' : 'false');

      const btn = $('batch-submit-btn');
      btn.disabled = true;
      btn.textContent = 'Processing CSV...';
      try {
        const res = await apiFetch('/api/batch/analyze', { method: 'POST', body: fd });
        state.batchResults = res.results || [];
        renderBatchResults(res);
        showToast(`Batch finished: ${res.succeeded} succeeded, ${res.failed} failed.`, 'success');
        if (res.saved_to_history) loadDashboard();
      } catch (err) {
        $('batch-error').textContent = err.message;
        $('batch-error').hidden = false;
      } finally {
        btn.disabled = false;
        btn.textContent = 'Run Batch Analysis →';
      }
    });

    $('batch-export-btn')?.addEventListener('click', () => {
      if (!state.batchResults.length) return;
      const cols = ['row', 'crop', 'soil_type', 'nitrogen', 'phosphorus', 'potassium', 'ph', 'moisture', 'fertilizer', 'score'];
      const lines = [
        cols.join(','),
        ...state.batchResults.map((r) => cols.map((c) => JSON.stringify(r[c] ?? '')).join(',')),
      ];
      const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
      triggerBlobDownload(blob, 'agri_nova_batch_predictions.csv');
    });

    $('sa-pdf-btn')?.addEventListener('click', downloadCurrentPDF);
    $('sa-tag-btn')?.addEventListener('click', downloadCurrentSampleTag);
    $('sa-speak-btn')?.addEventListener('click', speakCurrentSummary);
    $('sa-csv-btn')?.addEventListener('click', exportReportsCSV);
    $('sa-print-btn')?.addEventListener('click', () => window.print());
    $('sa-ask-ai-btn')?.addEventListener('click', () => {
      toggleChatbot(true);
      sendChatMessage('What is my soil analysis?');
    });

    setupIotStream();
  }

  // ==========================================
  // SOIL PH AVAILABILITY MATRIX & VOICE SUMMARY
  // ==========================================

  function renderPhAvailabilityMatrix(container, rawPh) {
    if (!container) return;
    const ph = Math.max(4.0, Math.min(9.0, Number(rawPh) || 6.5));
    const pct = ((ph - 4.0) / 5.0) * 100;
    const badge = $('sa-ph-zone-badge');

    let zoneText = 'Optimal Neutral Zone';
    let zoneNote = 'Most primary macronutrients (N, P, K) remain well available in the pH 6.0–7.5 band.';
    if (ph < 5.5) {
      zoneText = 'Acidic Risk Zone (< 5.5)';
      zoneNote = 'Strongly acidic soil can lock up Phosphorus and Calcium while increasing Aluminum/Manganese solubility. Discuss agricultural lime concepts with a lab.';
    } else if (ph > 7.8) {
      zoneText = 'Alkaline Risk Zone (> 7.8)';
      zoneNote = 'Alkaline conditions reduce Phosphorus, Iron, and Zinc availability. Confirm organic matter and micronutrient status via a lab test.';
    }
    if (badge) badge.textContent = `pH ${Number(rawPh).toFixed(1)} · ${zoneText}`;

    container.replaceChildren();
    const scaleWrap = document.createElement('div');
    scaleWrap.className = 'ph-scale-wrap';
    const bar = document.createElement('div');
    bar.className = 'ph-gradient-bar';
    const marker = document.createElement('div');
    marker.className = 'ph-marker';
    marker.style.left = `${pct}%`;
    marker.title = `Entered pH: ${rawPh}`;
    bar.appendChild(marker);
    const labels = document.createElement('div');
    labels.className = 'ph-labels';
    ['4.0 Acidic', '5.5', '6.5 Optimal', '7.5', '9.0 Alkaline'].forEach((t) => {
      const s = document.createElement('span');
      s.textContent = t;
      labels.appendChild(s);
    });
    scaleWrap.append(bar, labels);

    const grid = document.createElement('div');
    grid.className = 'ph-nutrient-grid';
    [
      ['Nitrogen (N)', ph >= 5.8 && ph <= 8.0 ? 'Good' : 'Reduced'],
      ['Phosphorus (P)', ph >= 6.0 && ph <= 7.5 ? 'Good' : 'Fixation Risk'],
      ['Potassium (K)', ph >= 5.5 ? 'Good' : 'Leach Risk'],
      ['Iron / Zinc', ph <= 7.5 ? 'Available' : 'Alkaline Lockup'],
    ].forEach(([nName, status]) => {
      const card = document.createElement('div');
      card.className = 'ph-nutrient-item';
      const st = document.createElement('strong');
      st.textContent = nName;
      const pill = document.createElement('span');
      pill.className = `status-tag ${status === 'Good' || status === 'Available' ? 'status-normal' : 'status-high'}`;
      pill.textContent = status;
      card.append(st, pill);
      grid.appendChild(card);
    });

    const noteP = document.createElement('p');
    noteP.className = 'muted-note';
    noteP.textContent = zoneNote;
    container.append(scaleWrap, grid, noteP);
  }

  function speakCurrentSummary() {
    if (!('speechSynthesis' in window)) {
      showToast('Read-aloud is not supported in this browser.', 'warning');
      return;
    }
    const btn = $('sa-speak-btn');
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
      if (btn) btn.textContent = '🔊 Listen to Summary';
      return;
    }
    if (!state.latestAnalysis) return;
    const r = state.latestAnalysis;
    const msg = new SpeechSynthesisUtterance(
      `Agri Nova AI soil summary for ${r.crop} on ${r.soil_type} soil. ` +
      `Prototype soil match index is ${r.score} out of 100. ` +
      `The Random Forest model predicted ${r.fertilizer}. ` +
      `${r.health?.note || ''} Please verify with a certified agricultural expert.`
    );
    msg.onend = () => {
      if (btn) btn.textContent = '🔊 Listen to Summary';
    };
    if (btn) btn.textContent = '⏹ Stop Audio';
    window.speechSynthesis.speak(msg);
  }

  async function downloadCurrentSampleTag() {
    if (!state.latestAnalysis || !state.latestInputs) {
      showToast('Complete a soil analysis first.', 'warning');
      return;
    }
    try {
      const response = await fetch('/api/report/sample-tag', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          report_uid: state.latestAnalysis.report_uid || '',
          crop: state.latestAnalysis.crop,
          soil_type: state.latestAnalysis.soil_type,
          plot_name: state.latestAnalysis.plot_name || '',
          date: state.latestAnalysis.date || '',
        }),
      });
      if (!response.ok) throw new Error('Could not generate sample tag PDF.');
      const blob = await response.blob();
      triggerBlobDownload(blob, 'Agri_Nova_Soil_Sample_Tag.pdf');
      showToast('Printable sample bag tag downloaded.', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // ==========================================
  // IOT SENSOR TELEMETRY
  // ==========================================

  let iotStreamInterval = null;
  let latestIotReading = null;

  function renderIotState(data) {
    const latest = data.latest;
    latestIotReading = latest;
    const loadBtn = $('iot-load-into-form-btn');
    if (latest) {
      $('iot-device').textContent = `${latest.device_id} (${latest.soil_type})`;
      $('iot-time').textContent = `${latest.display_time}${latest.is_simulated ? ' · Simulated' : ' · Live'}`;
      $('iot-env').textContent = `${formatTemp(latest.temperature)} / ${latest.humidity}%`;
      $('iot-moist-ph').textContent = `${latest.moisture}% / pH ${latest.ph}`;
      $('iot-npk').textContent = `${latest.nitrogen}-${latest.phosphorus}-${latest.potassium}`;
      if (loadBtn) loadBtn.disabled = false;
    }

    const list = $('iot-history-list');
    if (!list) return;
    list.replaceChildren();
    if (!data.history || !data.history.length) {
      const p = document.createElement('p');
      p.className = 'muted-text';
      p.textContent = 'No sensor packets received yet.';
      list.appendChild(p);
      return;
    }
    data.history.slice(0, 5).forEach((item) => {
      const row = document.createElement('div');
      row.className = 'recent-row';
      const left = document.createElement('div');
      const title = document.createElement('strong');
      title.textContent = `${item.device_id} · ${item.soil_type} · NPK ${item.nitrogen}/${item.phosphorus}/${item.potassium}`;
      const sub = document.createElement('small');
      sub.textContent = `${item.display_time} · Moisture ${item.moisture}% · pH ${item.ph}${item.is_simulated ? ' (Simulated)' : ''}`;
      left.append(title, sub);
      row.appendChild(left);
      list.appendChild(row);
    });
  }

  async function loadLatestIot() {
    try {
      const data = await apiFetch('/api/iot/latest');
      renderIotState(data);
    } catch {
      // Non-fatal
    }
  }

  async function pushSimulatedIot() {
    try {
      await apiFetch('/api/iot/simulate', {
        method: 'POST',
        body: JSON.stringify({ soil_type: $('sa-soil-type')?.value || 'Loamy' }),
      });
      await loadLatestIot();
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  function setupIotStream() {
    $('iot-sim-once-btn')?.addEventListener('click', async () => {
      await pushSimulatedIot();
      $('iot-mode-badge').textContent = 'SIMULATED PACKET';
      showToast('Simulated IoT sensor reading received.', 'info');
    });

    $('iot-stream-toggle-btn')?.addEventListener('click', () => {
      const btn = $('iot-stream-toggle-btn');
      if (iotStreamInterval) {
        clearInterval(iotStreamInterval);
        iotStreamInterval = null;
        btn.textContent = 'Start Simulated Stream';
        $('iot-mode-badge').textContent = 'PAUSED';
      } else {
        pushSimulatedIot();
        iotStreamInterval = setInterval(pushSimulatedIot, 4000);
        btn.textContent = 'Stop Simulated Stream';
        $('iot-mode-badge').textContent = 'SIMULATED STREAMING';
      }
    });

    $('iot-load-into-form-btn')?.addEventListener('click', () => {
      if (!latestIotReading) return;
      $('sa-soil-type').value = latestIotReading.soil_type;
      $('sa-temperature').value = state.units === 'imperial'
        ? ((latestIotReading.temperature * 9) / 5 + 32).toFixed(1)
        : latestIotReading.temperature;
      $('sa-humidity').value = latestIotReading.humidity;
      $('sa-moisture').value = latestIotReading.moisture;
      $('sa-nitrogen').value = latestIotReading.nitrogen;
      $('sa-phosphorus').value = latestIotReading.phosphorus;
      $('sa-potassium').value = latestIotReading.potassium;
      $('sa-ph').value = latestIotReading.ph;
      setSoilMode('single');
      showToast('Loaded latest sensor packet into Soil Analysis form.', 'success');
    });
  }

  async function runWhatIfSimulation() {
    if (!state.latestInputs) return;
    try {
      const simRes = await apiFetch('/api/analyze/simulate', {
        method: 'POST',
        body: JSON.stringify({
          crop: state.latestInputs.crop,
          soil_type: state.latestInputs.soil_type,
          temperature: state.latestInputs.temperature,
          humidity: state.latestInputs.humidity,
          moisture: state.latestInputs.moisture,
          nitrogen: $('sim-n').value,
          phosphorus: $('sim-p').value,
          potassium: $('sim-k').value,
          ph: $('sim-ph').value,
        }),
      });
      $('sim-fert-out').textContent = simRes.fertilizer;
      $('sim-score-out').textContent = `${simRes.score}/100`;
    } catch {
      // Ignore transient slider error
    }
  }

  function renderBatchResults(res) {
    $('batch-results-card').hidden = false;
    $('batch-summary-heading').textContent = `Processed ${res.processed} row(s): ${res.succeeded} valid, ${res.failed} error(s)${res.saved_to_history ? ' · Saved to History' : ''}`;

    const errBox = $('batch-errors-list');
    if (res.errors && res.errors.length) {
      errBox.hidden = false;
      errBox.textContent = res.errors.map((e) => `Row ${e.row}: ${e.error}`).join(' | ');
    } else {
      errBox.hidden = true;
    }

    const tbody = $('batch-tbody');
    tbody.replaceChildren();
    (res.results || []).forEach((item) => {
      const tr = document.createElement('tr');
      [
        item.row,
        item.crop,
        item.soil_type,
        `${item.nitrogen} / ${item.phosphorus} / ${item.potassium}`,
        item.ph,
        `${item.moisture}%`,
        item.fertilizer,
        `${item.score}/100`,
      ].forEach((val, idx) => {
        const td = document.createElement('td');
        if (idx === 6) {
          const span = document.createElement('span');
          span.className = 'badge-pill';
          span.textContent = String(val);
          td.appendChild(span);
        } else {
          td.textContent = String(val);
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
  }

  async function attachWeatherAdvisoryToSoil() {
    const city = $('weather-city-input')?.value?.trim() || 'Bengaluru';
    try {
      const w = state.weatherData || await apiFetch(`/api/weather?city=${encodeURIComponent(city)}`);
      const topAdv = (w.advisories || [])[0];
      if (!topAdv) return;
      $('sa-weather-advisory-box').hidden = false;
      $('sa-weather-adv-badge').textContent = `${w.city} · ${w.is_live ? 'LIVE' : 'DEMO'}`;
      $('sa-weather-adv-text').textContent = `${topAdv.title}: ${topAdv.detail}`;
    } catch {
      $('sa-weather-advisory-box').hidden = true;
    }
  }

  function renderSoilResult(result) {
    $('sa-empty').hidden = true;
    $('sa-result').hidden = false;
    $('sa-status-badge').textContent = result.report_uid || 'REPORT READY';
    $('sa-score').textContent = result.score;
    $('sa-fertilizer').textContent = result.fertilizer;

    const chips = $('sa-profile-chips');
    chips.replaceChildren();
    const inp = result.inputs || {};
    [
      result.plot_name ? `Plot: ${result.plot_name}` : null,
      `Crop: ${result.crop}`,
      `Soil: ${result.soil_type}`,
      `Temp: ${formatTemp(inp.temperature)}`,
      `Humidity: ${inp.humidity ?? '--'}%`,
      `Moisture: ${inp.moisture ?? '--'}%`,
      `pH: ${inp.ph ?? '--'}`,
    ].filter(Boolean).forEach((txt) => {
      const span = document.createElement('span');
      span.className = 'chip';
      span.textContent = txt;
      chips.appendChild(span);
    });

    // Sync simulator sliders
    if ($('sim-n')) {
      $('sim-n').value = Math.min(200, Number(inp.nitrogen) || 37);
      $('sim-p').value = Math.min(150, Number(inp.phosphorus) || 18);
      $('sim-k').value = Math.min(150, Number(inp.potassium) || 25);
      $('sim-ph').value = Number(inp.ph) || 6.5;
      $('sim-n-val').textContent = $('sim-n').value;
      $('sim-p-val').textContent = $('sim-p').value;
      $('sim-k-val').textContent = $('sim-k').value;
      $('sim-ph-val').textContent = $('sim-ph').value;
      $('sim-fert-out').textContent = result.fertilizer;
      $('sim-score-out').textContent = `${result.score}/100`;
    }

    renderTreeVotes($('sa-tree-votes'), result.tree_vote_distribution || []);
    attachWeatherAdvisoryToSoil();
    renderPhAvailabilityMatrix($('sa-ph-matrix'), inp.ph);
    renderNpkBars($('sa-npk-bars'), result.gaps || []);
    renderSoilRadarChart(result.gaps || []);

    const health = result.health || {};
    $('sa-health-overall').textContent = health.overall || 'Reviewed';
    $('sa-health-note').textContent = health.note || '';

    const obsWrap = $('sa-health-observations');
    obsWrap.replaceChildren();
    (health.observations || []).forEach((obs) => {
      const card = document.createElement('div');
      card.className = 'obs-item';
      const head = document.createElement('div');
      head.className = 'obs-item-head';
      const t = document.createElement('strong');
      t.textContent = obs.title;
      const s = document.createElement('span');
      const norm = String(obs.status || '').toLowerCase();
      s.className = `status-tag ${norm.includes('low') ? 'status-low' : norm.includes('high') ? 'status-high' : 'status-normal'}`;
      s.textContent = obs.status;
      head.append(t, s);
      const p = document.createElement('p');
      p.textContent = obs.detail;
      card.append(head, p);
      obsWrap.appendChild(card);
    });

    const actList = $('sa-actions');
    actList.replaceChildren();
    (result.actions || []).forEach((a) => {
      const li = document.createElement('li');
      li.textContent = a;
      actList.appendChild(li);
    });

    $('sa-disclaimer').textContent = result.disclaimer || '';
  }

  async function downloadCurrentPDF() {
    if (!state.latestAnalysis || !state.latestInputs) {
      showToast('Complete a soil analysis before downloading the PDF.', 'warning');
      return;
    }
    const btn = $('sa-pdf-btn');
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Generating QR PDF...';
    }
    try {
      const response = await fetch('/api/report/pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          inputs: state.latestInputs,
          result: state.latestAnalysis,
        }),
      });
      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || 'PDF generation failed.');
      }
      const blob = await response.blob();
      triggerBlobDownload(blob, 'Agri_Nova_AI_Soil_Report.pdf');
      showToast('QR-verified PDF report downloaded.', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.textContent = '↓ Download QR PDF Report';
      }
    }
  }

  // ==========================================
  // CROP RECOMMENDATION
  // ==========================================

  function setupCropRecommendation() {
    const form = $('crop-rec-form');
    if (!form) return;

    $('cr-copy-soil-btn')?.addEventListener('click', () => {
      $('cr-soil-type').value = $('sa-soil-type').value;
      $('cr-temperature').value = $('sa-temperature').value;
      $('cr-humidity').value = $('sa-humidity').value;
      $('cr-moisture').value = $('sa-moisture').value;
      $('cr-ph').value = $('sa-ph').value;
      $('cr-nitrogen').value = $('sa-nitrogen').value;
      $('cr-phosphorus').value = $('sa-phosphorus').value;
      $('cr-potassium').value = $('sa-potassium').value;
      showToast('Copied values from Soil Analysis form.', 'info');
    });

    $('cr-reset-btn')?.addEventListener('click', () => {
      form.reset();
      $('cr-error').hidden = true;
      $('cr-empty').hidden = false;
      $('cr-result').hidden = true;
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      $('cr-error').hidden = true;

      const btn = $('cr-submit-btn');
      btn.disabled = true;
      btn.textContent = 'Evaluating Suitability...';

      try {
        const data = await apiFetch('/api/crop-recommend', {
          method: 'POST',
          body: JSON.stringify({
            soil_type: $('cr-soil-type').value,
            temperature: $('cr-temperature').value,
            humidity: $('cr-humidity').value,
            moisture: $('cr-moisture').value,
            ph: $('cr-ph').value,
            nitrogen: $('cr-nitrogen').value,
            phosphorus: $('cr-phosphorus').value,
            potassium: $('cr-potassium').value,
            temp_unit: state.units === 'imperial' ? 'F' : 'C',
          }),
        });

        $('cr-empty').hidden = true;
        $('cr-result').hidden = false;
        $('cr-top-crop').textContent = data.suggested_crop;
        $('cr-top-reason').textContent = data.reason;
        $('cr-top-score').textContent = data.suitability_score;
        $('cr-score-basis').textContent = data.score_basis;
        $('cr-soil-summary').textContent = data.soil_condition_summary;
        $('cr-disclaimer').textContent = data.disclaimer;

        const candWrap = $('cr-candidates');
        candWrap.replaceChildren();
        (data.top_matches || []).forEach((cand) => {
          const row = document.createElement('div');
          row.className = 'candidate-row';
          const head = document.createElement('div');
          head.className = 'candidate-head';
          const name = document.createElement('strong');
          name.textContent = cand.crop;
          const score = document.createElement('span');
          score.className = 'badge-pill';
          score.textContent = `${cand.suitability_score}/100 pts`;
          head.append(name, score);
          const desc = document.createElement('p');
          desc.className = 'muted-text';
          desc.textContent = cand.summary;
          row.append(head, desc);
          candWrap.appendChild(row);
        });

        const consList = $('cr-considerations');
        consList.replaceChildren();
        (data.considerations || []).forEach((c) => {
          const li = document.createElement('li');
          li.textContent = c;
          consList.appendChild(li);
        });

        loadCropStages(data.suggested_crop);
      } catch (err) {
        $('cr-error').textContent = err.message;
        $('cr-error').hidden = false;
      } finally {
        btn.disabled = false;
        btn.textContent = 'Evaluate Crop Suitability →';
      }
    });

    document.querySelectorAll('.stage-crop-pill').forEach((pill) => {
      pill.addEventListener('click', () => loadCropStages(pill.dataset.stageCrop));
    });
    loadCropStages('Rice');
  }

  async function loadCropStages(cropName) {
    document.querySelectorAll('.stage-crop-pill').forEach((p) => {
      p.classList.toggle('active', p.dataset.stageCrop === cropName);
    });
    try {
      const data = await apiFetch(`/api/crop-stages?crop=${encodeURIComponent(cropName)}`);
      $('cr-stage-meta').textContent = `${data.crop} · Typical pH ${data.ph_range} · ${data.moisture_note}`;
      const grid = $('cr-stages-grid');
      grid.replaceChildren();
      (data.stages || []).forEach((st) => {
        const card = document.createElement('div');
        card.className = 'stage-card';
        const win = document.createElement('small');
        win.textContent = `${st.window} · ${st.focus}`;
        const h4 = document.createElement('h4');
        h4.textContent = st.stage;
        const p = document.createElement('p');
        p.textContent = st.note;
        card.append(win, h4, p);
        grid.appendChild(card);
      });
    } catch {
      // Non-fatal
    }
  }

  // ==========================================
  // FERTILIZER GUIDE
  // ==========================================

  async function loadFertilizerGuide(search = '', nutrient = 'all') {
    try {
      const params = new URLSearchParams({ q: search, nutrient });
      const data = await apiFetch(`/api/fertilizers?${params.toString()}`);
      state.guideItems = data.items || [];
      renderFertilizerGrid();
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  function renderFertilizerGrid() {
    const grid = $('fg-grid');
    grid.replaceChildren();

    if (!state.guideItems.length) {
      const empty = document.createElement('div');
      empty.className = 'empty-card';
      empty.textContent = 'No fertilizers matched your search filter.';
      grid.appendChild(empty);
      return;
    }

    state.guideItems.forEach((item) => {
      const card = document.createElement('article');
      card.className = 'guide-card';

      const topBadge = document.createElement('span');
      topBadge.className = 'badge-pill';
      topBadge.textContent = `${item.category} · ${item.primary_nutrient}`;

      const h3 = document.createElement('h3');
      h3.textContent = item.name;

      const comp = document.createElement('div');
      comp.className = 'guide-meta';
      comp.textContent = item.composition;

      const purpose = document.createElement('p');
      purpose.textContent = item.purpose;

      const benTitle = document.createElement('strong');
      benTitle.style.fontSize = '12px';
      benTitle.textContent = 'Key Benefits';
      const benUl = document.createElement('ul');
      benUl.className = 'guide-list';
      item.benefits.forEach((b) => {
        const li = document.createElement('li');
        li.textContent = b;
        benUl.appendChild(li);
      });

      const precTitle = document.createElement('strong');
      precTitle.style.fontSize = '12px';
      precTitle.textContent = 'Precautions & Soil-Test Context';
      const precP = document.createElement('p');
      precP.className = 'muted-text';
      precP.textContent = `${item.precautions[0]} ${item.soil_test_context}`;

      const footer = document.createElement('div');
      footer.className = 'guide-card-footer';
      const selected = state.compareIds.includes(item.id);
      const cmpBtn = document.createElement('button');
      cmpBtn.type = 'button';
      cmpBtn.className = selected ? 'btn-primary btn-xs' : 'btn-outline btn-xs';
      cmpBtn.textContent = selected ? 'Selected for Compare ✓' : '+ Compare';
      cmpBtn.addEventListener('click', () => toggleCompareFertilizer(item.id));
      footer.appendChild(cmpBtn);

      card.append(topBadge, h3, comp, purpose, benTitle, benUl, precTitle, precP, footer);
      grid.appendChild(card);
    });
  }

  function toggleCompareFertilizer(id) {
    const idx = state.compareIds.indexOf(id);
    if (idx >= 0) {
      state.compareIds.splice(idx, 1);
    } else {
      if (state.compareIds.length >= 3) {
        showToast('Select up to 3 fertilizers to compare side by side.', 'warning');
        return;
      }
      state.compareIds.push(id);
    }
    renderFertilizerGrid();
    renderComparePanel();
  }

  function renderComparePanel() {
    const bar = $('fg-compare-bar');
    if (!state.compareIds.length) {
      bar.hidden = true;
      return;
    }
    bar.hidden = false;
    $('fg-compare-count').textContent = state.compareIds.length;

    const selected = state.guideItems.filter((g) => state.compareIds.includes(g.id));
    const table = document.createElement('table');
    table.className = 'data-table';
    const thead = document.createElement('thead');
    const hRow = document.createElement('tr');
    const firstTh = document.createElement('th');
    firstTh.textContent = 'Attribute';
    hRow.appendChild(firstTh);
    selected.forEach((s) => {
      const th = document.createElement('th');
      th.textContent = s.name;
      hRow.appendChild(th);
    });
    thead.appendChild(hRow);

    const tbody = document.createElement('tbody');
    [
      ['Composition', (s) => s.composition],
      ['Primary Nutrient', (s) => s.primary_nutrient],
      ['Agricultural Purpose', (s) => s.purpose],
      ['Precautions', (s) => s.precautions.join(' ')],
      ['Soil-Test Context', (s) => s.soil_test_context],
    ].forEach(([label, getter]) => {
      const tr = document.createElement('tr');
      const tdLabel = document.createElement('td');
      const strong = document.createElement('strong');
      strong.textContent = label;
      tdLabel.appendChild(strong);
      tr.appendChild(tdLabel);
      selected.forEach((s) => {
        const td = document.createElement('td');
        td.textContent = getter(s);
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });

    table.append(thead, tbody);
    $('fg-compare-table-wrap').replaceChildren(table);
  }

  function setupFertilizerGuide() {
    let activeNutrient = 'all';
    $('fg-search')?.addEventListener('input', (e) => {
      loadFertilizerGuide(e.target.value, activeNutrient);
    });
    $('fg-filters')?.addEventListener('click', (e) => {
      const btn = e.target.closest('.filter-pill');
      if (!btn) return;
      activeNutrient = btn.dataset.nutrient || 'all';
      document.querySelectorAll('#fg-filters .filter-pill').forEach((b) => {
        b.classList.toggle('active', b === btn);
      });
      loadFertilizerGuide($('fg-search').value, activeNutrient);
    });
    $('fg-clear-compare')?.addEventListener('click', () => {
      state.compareIds = [];
      renderComparePanel();
      renderFertilizerGrid();
    });
  }

  // ==========================================
  // WEATHER MODULE
  // ==========================================

  async function loadWeather(city) {
    $('weather-error').hidden = true;
    $('weather-loading').hidden = false;
    $('weather-content').hidden = true;
    $('weather-status-banner').hidden = true;

    try {
      const data = await apiFetch(`/api/weather?city=${encodeURIComponent(city)}`);
      state.weatherData = data;
      state.weatherLoaded = true;
      renderWeatherData(data);
    } catch (err) {
      $('weather-error').textContent = err.message;
      $('weather-error').hidden = false;
    } finally {
      $('weather-loading').hidden = true;
    }
  }

  function renderWeatherData(data) {
    if (!data) return;
    $('weather-content').hidden = false;

    const banner = $('weather-status-banner');
    banner.hidden = false;
    banner.textContent = data.is_live
      ? data.status_message
      : `${data.status_message} ${data.setup_instructions || ''}`;

    $('weather-mode-badge').textContent = data.is_live ? 'LIVE WEATHER' : 'DEMO DATA (OFFLINE)';
    $('weather-location').textContent = `${data.city}${data.country ? `, ${data.country}` : ''}`;
    $('weather-condition').textContent = data.description || data.condition;
    $('weather-updated').textContent = `Updated: ${data.updated_at}`;
    $('weather-temp').textContent = formatTemp(data.temperature_c);
    $('weather-feels').textContent = `Feels like ${formatTemp(data.feels_like_c)}`;
    $('weather-humidity').textContent = `${data.humidity}%`;
    $('weather-wind').textContent = `${data.wind_speed_kmh} km/h`;
    $('weather-rain').textContent = `${data.rain_probability}%`;
    $('weather-source-label').textContent = data.is_live ? 'Live API' : 'Demo Mode';
    $('weather-source-sub').textContent = data.is_live ? 'OpenWeatherMap' : 'Configure OPENWEATHER_API_KEY';

    const advList = $('weather-advisories-list');
    if (advList) {
      advList.replaceChildren();
      (data.advisories || []).forEach((adv) => {
        const row = document.createElement('div');
        row.className = `tip-row level-${adv.level || 'info'}`;
        const t = document.createElement('strong');
        t.textContent = adv.title;
        const p = document.createElement('p');
        p.textContent = adv.detail;
        row.append(t, p);
        advList.appendChild(row);
      });
    }

    const fcGrid = $('weather-forecast-grid');
    fcGrid.replaceChildren();
    (data.forecast || []).forEach((slot) => {
      const card = document.createElement('div');
      card.className = 'forecast-item';
      const lbl = document.createElement('small');
      lbl.textContent = slot.label;
      const tmp = document.createElement('strong');
      tmp.textContent = formatTemp(slot.temp_c);
      const cond = document.createElement('span');
      cond.textContent = `${slot.condition} · Rain ${slot.rain_prob}%`;
      card.append(lbl, tmp, cond);
      fcGrid.appendChild(card);
    });
  }

  function setupWeather() {
    $('weather-form')?.addEventListener('submit', (e) => {
      e.preventDefault();
      const city = $('weather-city-input').value.trim();
      if (!city) {
        showToast('Enter a city name first.', 'warning');
        return;
      }
      loadWeather(city);
    });

    document.querySelectorAll('.city-chip').forEach((btn) => {
      btn.addEventListener('click', () => {
        const city = btn.dataset.city;
        $('weather-city-input').value = city;
        loadWeather(city);
      });
    });
  }

  // ==========================================
  // CHATBOT
  // ==========================================

  function renderChatStreams(typing = false) {
    [$('chatbot-messages'), $('page-chat-messages')].forEach((container) => {
      if (!container) return;
      container.replaceChildren();
      state.chatMessages.forEach((msg) => {
        const bubble = document.createElement('div');
        bubble.className = msg.role === 'user' ? 'user-message' : 'bot-message';
        bubble.textContent = msg.text;
        container.appendChild(bubble);
      });
      if (typing) {
        const typingBubble = document.createElement('div');
        typingBubble.className = 'bot-message';
        const dots = document.createElement('div');
        dots.className = 'typing-dots';
        dots.append(document.createElement('span'), document.createElement('span'), document.createElement('span'));
        typingBubble.appendChild(dots);
        container.appendChild(typingBubble);
      }
      container.scrollTop = container.scrollHeight;
    });
  }

  function toggleChatbot(forceOpen = null) {
    const win = $('chatbot-window');
    if (!win) return;
    const shouldOpen = forceOpen !== null ? forceOpen : win.classList.contains('chatbot-hidden');
    win.classList.toggle('chatbot-hidden', !shouldOpen);
    if (shouldOpen) $('chatbot-input')?.focus();
  }

  async function sendChatMessage(rawText) {
    const text = (rawText || '').trim();
    if (!text) return;

    state.chatMessages.push({ role: 'user', text });
    renderChatStreams(true);

    try {
      const res = await apiFetch('/api/chat', {
        method: 'POST',
        body: JSON.stringify({
          message: text,
          latest_analysis: state.latestAnalysis,
        }),
      });
      state.chatMessages.push({ role: 'bot', text: res.reply });
    } catch (err) {
      state.chatMessages.push({ role: 'bot', text: `Assistant error: ${err.message}` });
    } finally {
      renderChatStreams(false);
    }
  }

  function clearChat() {
    state.chatMessages = [
      {
        role: 'bot',
        text: 'Chat cleared. Ask me about your latest soil analysis, NPK nutrients, fertilizers, or crops.',
      },
    ];
    renderChatStreams(false);
  }

  function setupChatbot() {
    renderChatStreams(false);

    $('chatbot-toggle')?.addEventListener('click', () => toggleChatbot());
    $('chatbot-close')?.addEventListener('click', () => toggleChatbot(false));
    $('chatbot-clear')?.addEventListener('click', clearChat);
    $('page-chat-clear')?.addEventListener('click', clearChat);

    $('chatbot-form')?.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = $('chatbot-input');
      const val = input.value.trim();
      if (!val) return;
      input.value = '';
      sendChatMessage(val);
    });

    $('page-chat-form')?.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = $('page-chat-input');
      const val = input.value.trim();
      if (!val) return;
      input.value = '';
      sendChatMessage(val);
    });

    document.querySelectorAll('.quick-question, .quick-q-chip').forEach((btn) => {
      btn.addEventListener('click', () => {
        sendChatMessage(btn.dataset.q || btn.textContent);
      });
    });

    bindVoiceMic($('chatbot-mic-btn'), $('chatbot-input'));
    bindVoiceMic($('page-chat-mic-btn'), $('page-chat-input'));
  }

  function bindVoiceMic(btn, inputEl) {
    if (!btn || !inputEl) return;
    btn.addEventListener('click', () => {
      const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRec) {
        showToast('Voice recognition is unavailable in this browser (supported in Chrome/Edge).', 'warning');
        return;
      }
      const recognition = new SpeechRec();
      recognition.lang = state.lang === 'hi' ? 'hi-IN' : state.lang === 'kn' ? 'kn-IN' : 'en-IN';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;
      btn.classList.add('listening');
      recognition.onresult = (event) => {
        const transcript = event.results[0]?.[0]?.transcript || '';
        inputEl.value = transcript;
        if (transcript.trim()) sendChatMessage(transcript);
      };
      recognition.onerror = () => showToast('Could not capture voice input.', 'warning');
      recognition.onend = () => btn.classList.remove('listening');
      recognition.start();
    });
  }

  // ==========================================
  // REPORTS HISTORY + MULTI-REPORT COMPARISON
  // ==========================================

  function updateCompareButton() {
    const btn = $('rh-compare-btn');
    if (!btn) return;
    const n = state.compareReportIds.length;
    btn.textContent = `Compare Selected (${n})`;
    btn.disabled = n < 2;
  }

  async function loadHistoryTable() {
    try {
      const params = new URLSearchParams({
        q: $('rh-search')?.value.trim() || '',
        crop: $('rh-crop-filter')?.value || 'all',
        plot_id: $('rh-plot-filter')?.value || 'all',
        sort: $('rh-sort')?.value || 'newest',
      });
      const reports = await apiFetch(`/api/history?${params.toString()}`);

      const tbody = $('rh-tbody');
      tbody.replaceChildren();
      $('rh-empty').hidden = reports.length > 0;
      $('rh-table-wrap').hidden = reports.length === 0;

      reports.forEach((rep) => {
        const tr = document.createElement('tr');

        const tdCmp = document.createElement('td');
        const cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.checked = state.compareReportIds.includes(rep.id);
        cb.setAttribute('aria-label', `Select ${rep.report_uid} for comparison`);
        cb.addEventListener('change', () => {
          if (cb.checked) {
            if (state.compareReportIds.length >= 4) {
              cb.checked = false;
              showToast('Select up to 4 reports to compare.', 'warning');
              return;
            }
            state.compareReportIds.push(rep.id);
          } else {
            state.compareReportIds = state.compareReportIds.filter((x) => x !== rep.id);
          }
          updateCompareButton();
        });
        tdCmp.appendChild(cb);

        const tdId = document.createElement('td');
        tdId.textContent = rep.report_uid || `#${rep.id}`;

        const tdPlot = document.createElement('td');
        tdPlot.textContent = rep.plot_name || '—';

        const tdCrop = document.createElement('td');
        const strongCrop = document.createElement('strong');
        strongCrop.textContent = rep.crop;
        tdCrop.appendChild(strongCrop);

        const tdSoil = document.createElement('td');
        tdSoil.textContent = rep.soil_type || 'Not recorded';

        const tdFert = document.createElement('td');
        const pill = document.createElement('span');
        pill.className = 'badge-pill';
        pill.textContent = rep.fertilizer || 'Not recorded';
        tdFert.appendChild(pill);

        const tdScore = document.createElement('td');
        tdScore.textContent = `${rep.score}/100`;

        const tdDate = document.createElement('td');
        tdDate.textContent = rep.date || '';

        const tdAct = document.createElement('td');
        const actWrap = document.createElement('div');
        actWrap.className = 'table-actions';

        const viewBtn = document.createElement('button');
        viewBtn.type = 'button';
        viewBtn.className = 'btn-outline btn-xs';
        viewBtn.textContent = 'Details';
        viewBtn.addEventListener('click', () => openReportDetailModal(rep.id));

        const pdfBtn = document.createElement('button');
        pdfBtn.type = 'button';
        pdfBtn.className = 'btn-outline btn-xs';
        pdfBtn.textContent = 'PDF';
        pdfBtn.addEventListener('click', () => downloadReportPdfById(rep.id, rep.report_uid));

        const delBtn = document.createElement('button');
        delBtn.type = 'button';
        delBtn.className = 'btn-danger-outline btn-xs';
        delBtn.textContent = 'Delete';
        delBtn.addEventListener('click', () => {
          openConfirmModal(
            'Delete Report',
            `Delete report ${rep.report_uid} (${rep.crop})? This cannot be undone.`,
            async () => {
              await apiFetch(`/api/history/${rep.id}`, { method: 'DELETE' });
              state.compareReportIds = state.compareReportIds.filter((x) => x !== rep.id);
              updateCompareButton();
              showToast('Report deleted.', 'success');
              loadHistoryTable();
              loadDashboard();
            }
          );
        });

        actWrap.append(viewBtn, pdfBtn, delBtn);
        tdAct.appendChild(actWrap);
        tr.append(tdCmp, tdId, tdPlot, tdCrop, tdSoil, tdFert, tdScore, tdDate, tdAct);
        tbody.appendChild(tr);
      });
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  async function openCompareReportsModal() {
    if (state.compareReportIds.length < 2) return;
    try {
      const data = await apiFetch(`/api/history/compare?ids=${state.compareReportIds.join(',')}`);
      const reps = data.reports || [];
      const table = document.createElement('table');
      table.className = 'data-table';

      const thead = document.createElement('thead');
      const hRow = document.createElement('tr');
      const firstTh = document.createElement('th');
      firstTh.textContent = 'Metric';
      hRow.appendChild(firstTh);
      reps.forEach((r) => {
        const th = document.createElement('th');
        th.textContent = `${r.report_uid} (${r.crop})`;
        hRow.appendChild(th);
      });
      thead.appendChild(hRow);

      const tbody = document.createElement('tbody');
      [
        ['Date', (r) => r.date || '—'],
        ['Field Plot', (r) => r.plot_name || '—'],
        ['Crop', (r) => r.crop],
        ['Soil Type', (r) => r.soil_type || 'Not recorded'],
        ['ML Fertilizer', (r) => r.fertilizer],
        ['Demo Match Index', (r) => `${r.score}/100`],
        ['Nitrogen (kg/ha*)', (r) => r.nitrogen ?? 'N/A'],
        ['Phosphorus (kg/ha*)', (r) => r.phosphorus ?? 'N/A'],
        ['Potassium (kg/ha*)', (r) => r.potassium ?? 'N/A'],
        ['Soil pH', (r) => r.ph ?? 'N/A'],
        ['Moisture (%)', (r) => (r.moisture !== null && r.moisture !== undefined ? `${r.moisture}%` : 'N/A')],
        ['Temperature', (r) => formatTemp(r.temperature)],
      ].forEach(([label, fn]) => {
        const tr = document.createElement('tr');
        const tdLbl = document.createElement('td');
        const strong = document.createElement('strong');
        strong.textContent = label;
        tdLbl.appendChild(strong);
        tr.appendChild(tdLbl);
        reps.forEach((r) => {
          const td = document.createElement('td');
          td.textContent = String(fn(r));
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });

      table.append(thead, tbody);
      $('cmp-body').replaceChildren(table);
      if ($('cmp-pdf-btn')) {
        $('cmp-pdf-btn').onclick = async () => {
          const resp = await fetch(`/api/history/compare/pdf?ids=${state.compareReportIds.join(',')}`);
          if (!resp.ok) {
            showToast('Could not generate Comparison PDF.', 'error');
            return;
          }
          const blob = await resp.blob();
          triggerBlobDownload(blob, 'Agri_Nova_AI_Comparison_Report.pdf');
          showToast('Comparison PDF downloaded.', 'success');
        };
      }
      $('compare-modal').hidden = false;
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  async function openReportDetailModal(reportId) {
    try {
      const rep = await apiFetch(`/api/history/${reportId}`);
      $('rm-uid').textContent = rep.report_uid || `REPORT #${rep.id}`;
      $('rm-title').textContent = `${rep.crop} — ${rep.fertilizer}`;

      const body = $('rm-body');
      body.replaceChildren();

      const meta = document.createElement('div');
      meta.className = 'profile-chips';
      [
        `Date: ${rep.date}`,
        rep.plot_name ? `Plot: ${rep.plot_name}` : null,
        `Soil Type: ${rep.soil_type || 'Not recorded'}`,
        `Match Index: ${rep.score}/100`,
        `N: ${rep.nitrogen ?? 'N/A'}`,
        `P: ${rep.phosphorus ?? 'N/A'}`,
        `K: ${rep.potassium ?? 'N/A'}`,
        `pH: ${rep.ph ?? 'N/A'}`,
        `Moisture: ${rep.moisture ?? 'N/A'}%`,
      ].filter(Boolean).forEach((text) => {
        const chip = document.createElement('span');
        chip.className = 'chip';
        chip.textContent = text;
        meta.appendChild(chip);
      });
      body.appendChild(meta);

      if (rep.gaps && rep.gaps.length) {
        const barsBox = document.createElement('div');
        barsBox.className = 'sub-panel';
        renderNpkBars(barsBox, rep.gaps);
        body.appendChild(barsBox);
      }

      if (rep.actions && rep.actions.length) {
        const ul = document.createElement('ul');
        ul.className = 'check-list';
        rep.actions.forEach((a) => {
          const li = document.createElement('li');
          li.textContent = a;
          ul.appendChild(li);
        });
        body.appendChild(ul);
      }

      const disc = document.createElement('div');
      disc.className = 'alert-warning';
      disc.textContent = rep.disclaimer || 'Academic prototype report.';
      body.appendChild(disc);

      $('rm-pdf-btn').onclick = () => downloadReportPdfById(rep.id, rep.report_uid);
      if ($('rm-tag-btn')) {
        $('rm-tag-btn').onclick = async () => {
          const resp = await fetch(`/api/report/sample-tag/${rep.id}`);
          if (!resp.ok) {
            showToast('Could not generate sample tag.', 'error');
            return;
          }
          const blob = await resp.blob();
          triggerBlobDownload(blob, `Agri_Nova_Tag_${rep.report_uid}.pdf`);
          showToast('Sample bag tag PDF downloaded.', 'success');
        };
      }
      $('report-modal').hidden = false;
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  async function downloadReportPdfById(reportId, reportUid) {
    try {
      const response = await fetch(`/api/report/pdf/${reportId}`);
      if (!response.ok) throw new Error('Could not generate PDF.');
      const blob = await response.blob();
      triggerBlobDownload(blob, `Agri_Nova_AI_${reportUid || reportId}.pdf`);
      showToast('QR-verified PDF downloaded.', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  async function exportReportsCSV() {
    try {
      const response = await fetch('/api/history/export/csv');
      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || 'No reports available to export.');
      }
      const blob = await response.blob();
      triggerBlobDownload(blob, 'agri_nova_ai_reports.csv');
      showToast('CSV exported.', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  function confirmClearHistory() {
    openConfirmModal(
      'Clear Analysis History',
      'Delete all saved soil analysis records in your active workspace? Your original history.json backup file remains untouched on disk.',
      async () => {
        await apiFetch('/api/history/clear', { method: 'DELETE' });
        state.latestAnalysis = null;
        state.latestInputs = null;
        state.compareReportIds = [];
        updateCompareButton();
        showToast('Workspace history cleared.', 'success');
        loadDashboard();
        if (state.activeView === 'reports-history') loadHistoryTable();
      }
    );
  }

  function setupHistoryView() {
    $('rh-search')?.addEventListener('input', loadHistoryTable);
    $('rh-crop-filter')?.addEventListener('change', loadHistoryTable);
    $('rh-plot-filter')?.addEventListener('change', loadHistoryTable);
    $('rh-sort')?.addEventListener('change', loadHistoryTable);
    $('rh-compare-btn')?.addEventListener('click', openCompareReportsModal);
    $('rh-export-csv-btn')?.addEventListener('click', exportReportsCSV);
    $('rh-clear-btn')?.addEventListener('click', confirmClearHistory);

    $('rm-close')?.addEventListener('click', () => ($('report-modal').hidden = true));
    $('rm-close-btn')?.addEventListener('click', () => ($('report-modal').hidden = true));
    $('cmp-close')?.addEventListener('click', () => ($('compare-modal').hidden = true));
    $('cmp-close-btn')?.addEventListener('click', () => ($('compare-modal').hidden = true));

    $('open-dataset-modal-btn')?.addEventListener('click', () => {
      $('dataset-modal').hidden = false;
      loadDatasetExplorer();
    });
    $('ds-close')?.addEventListener('click', () => ($('dataset-modal').hidden = true));
    $('ds-close-btn')?.addEventListener('click', () => ($('dataset-modal').hidden = true));
    $('ds-crop-filter')?.addEventListener('change', loadDatasetExplorer);
    $('ds-fert-filter')?.addEventListener('change', loadDatasetExplorer);

    $('confirm-close')?.addEventListener('click', closeConfirmModal);
    $('confirm-cancel')?.addEventListener('click', closeConfirmModal);
    $('confirm-ok')?.addEventListener('click', async () => {
      const cb = state.confirmCallback;
      closeConfirmModal();
      if (cb) {
        try {
          await cb();
        } catch (err) {
          showToast(err.message, 'error');
        }
      }
    });
  }

  async function loadDatasetExplorer() {
    try {
      const params = new URLSearchParams({
        crop: $('ds-crop-filter')?.value || 'all',
        fertilizer: $('ds-fert-filter')?.value || 'all',
      });
      const data = await apiFetch(`/api/dataset-explorer?${params.toString()}`);
      $('ds-total-rows').textContent = data.total_rows;
      $('ds-test-rows').textContent = data.test_split_rows;
      $('ds-acc').textContent = `${data.holdout_accuracy_pct}%`;
      $('ds-caveat').textContent = data.validation_caveat;

      const tbody = $('ds-tbody');
      tbody.replaceChildren();
      (data.rows || []).forEach((row) => {
        const tr = document.createElement('tr');
        [
          row.row_id, row.crop_type, row.soil_type, row.temperature,
          row.humidity, row.moisture, row.nitrogen, row.phosphorous,
          row.potassium, row.fertilizer,
        ].forEach((val, idx) => {
          const td = document.createElement('td');
          if (idx === 9) {
            const sp = document.createElement('span');
            sp.className = 'badge-pill';
            sp.textContent = String(val);
            td.appendChild(sp);
          } else {
            td.textContent = String(val);
          }
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // ==========================================
  // PEST & CAMERA AI (LOCAL ONNX VISION)
  // ==========================================

  let pestStream = null;
  let pestImageBlob = null;
  let pestImageFilename = 'camera_snapshot.jpg';

  function stopPestCamera() {
    if (pestStream) {
      pestStream.getTracks().forEach((t) => t.stop());
      pestStream = null;
    }
    if ($('pest-video')) {
      $('pest-video').srcObject = null;
      $('pest-video').hidden = true;
    }
    if ($('pest-capture-btn')) $('pest-capture-btn').disabled = true;
    if ($('pest-stop-cam-btn')) $('pest-stop-cam-btn').disabled = true;
    if ($('pest-cam-status')) $('pest-cam-status').textContent = pestImageBlob ? 'IMAGE READY' : 'CAMERA IDLE';
  }

  function showPestPreview(blob, filename) {
    pestImageBlob = blob;
    pestImageFilename = filename || 'plant_photo.jpg';
    const img = $('pest-preview-img');
    const url = URL.createObjectURL(blob);
    img.onload = () => URL.revokeObjectURL(url);
    img.src = url;
    img.hidden = false;
    $('pest-stage-empty').hidden = true;
    $('pest-analyze-btn').disabled = false;
    $('pest-cam-status').textContent = 'IMAGE READY';
  }

  function setupPestCamera() {
    $('pest-start-cam-btn')?.addEventListener('click', async () => {
      $('pest-error').hidden = true;
      if (!navigator.mediaDevices?.getUserMedia) {
        $('pest-error').textContent = 'Live camera access is unavailable in this browser. Use Upload Photo instead.';
        $('pest-error').hidden = false;
        return;
      }
      try {
        stopPestCamera();
        pestStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' },
          audio: false,
        });
        const video = $('pest-video');
        video.srcObject = pestStream;
        video.hidden = false;
        $('pest-preview-img').hidden = true;
        $('pest-stage-empty').hidden = true;
        $('pest-capture-btn').disabled = false;
        $('pest-stop-cam-btn').disabled = false;
        $('pest-cam-status').textContent = 'CAMERA LIVE';
      } catch (err) {
        $('pest-error').textContent = `Camera permission error: ${err.message}. You can still upload a photo file.`;
        $('pest-error').hidden = false;
      }
    });

    $('pest-capture-btn')?.addEventListener('click', () => {
      const video = $('pest-video');
      const canvas = $('pest-canvas');
      if (!video || !video.videoWidth) return;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      canvas.toBlob((blob) => {
        if (!blob) return;
        stopPestCamera();
        showPestPreview(blob, 'camera_snapshot.jpg');
        showToast('Camera snapshot captured.', 'success');
      }, 'image/jpeg', 0.92);
    });

    $('pest-stop-cam-btn')?.addEventListener('click', () => {
      stopPestCamera();
      if (!pestImageBlob) $('pest-stage-empty').hidden = false;
    });

    $('pest-file-input')?.addEventListener('change', (e) => {
      const file = e.target.files?.[0];
      if (!file) return;
      stopPestCamera();
      showPestPreview(file, file.name);
      showToast('Image loaded for ONNX inspection.', 'info');
    });

    $('pest-analyze-btn')?.addEventListener('click', async () => {
      if (!pestImageBlob) return;
      $('pest-error').hidden = true;
      const btn = $('pest-analyze-btn');
      btn.disabled = true;
      btn.textContent = 'Running Local ONNX Vision...';

      const fd = new FormData();
      fd.append('image', pestImageBlob, pestImageFilename);
      fd.append('mode', $('pest-mode')?.value || 'auto_hybrid');
      fd.append('crop', $('pest-crop')?.value || 'Not specified');

      try {
        const res = await apiFetch('/api/pest/analyze', { method: 'POST', body: fd });
        renderPestResult(res);
        showToast(`Detected: ${res.primary_prediction.label}`, 'success');
        loadPestScans();
      } catch (err) {
        $('pest-error').textContent = err.message;
        $('pest-error').hidden = false;
      } finally {
        btn.disabled = false;
        btn.textContent = 'Analyze Photo with Local ONNX AI →';
      }
    });

    $('pest-guide-search')?.addEventListener('input', (e) => {
      loadPestGuide(e.target.value);
    });
  }

  function renderPestResult(res) {
    $('pest-result-empty').hidden = true;
    $('pest-result').hidden = false;

    const prim = res.primary_prediction;
    const ipm = res.ipm_guidance;
    $('pest-conf').textContent = prim.confidence_pct;
    $('pest-model-used').textContent = prim.model_used;
    $('pest-label').textContent = prim.label;
    $('pest-category').textContent = ipm.category;
    $('pest-severity-badge').textContent = ipm.severity;

    const canopy = res.canopy_metrics || {};
    const chips = $('pest-canopy-chips');
    chips.replaceChildren();
    [
      `Green Canopy: ${canopy.green_canopy_pct ?? 0}%`,
      `Yellow/Chlorosis: ${canopy.yellow_chlorosis_pct ?? 0}%`,
      `Brown/Spot: ${canopy.brown_lesion_pct ?? 0}%`,
    ].forEach((txt) => {
      const sp = document.createElement('span');
      sp.className = 'chip';
      sp.textContent = txt;
      chips.appendChild(sp);
    });

    $('pest-ipm-summary').textContent = ipm.summary;
    const cult = $('pest-cultural-list');
    cult.replaceChildren();
    (ipm.cultural || []).forEach((c) => {
      const li = document.createElement('li');
      li.textContent = c;
      cult.appendChild(li);
    });
    const bio = $('pest-bio-list');
    bio.replaceChildren();
    (ipm.biological || []).forEach((b) => {
      const li = document.createElement('li');
      li.textContent = b;
      bio.appendChild(li);
    });
    $('pest-pesticide-class').textContent = ipm.pesticide_class;
    $('pest-precaution').textContent = `Safety & Verification: ${ipm.precaution}`;

    const breakdown = $('pest-model-breakdown');
    breakdown.replaceChildren();
    Object.entries(res.model_breakdown || {}).forEach(([modelName, preds]) => {
      const card = document.createElement('div');
      card.className = 'obs-item';
      const head = document.createElement('div');
      head.className = 'obs-item-head';
      const strong = document.createElement('strong');
      strong.textContent = modelName;
      head.appendChild(strong);
      const p = document.createElement('p');
      p.textContent = (preds || []).map((x) => `${x.label} (${x.confidence_pct}%)`).join(' · ');
      card.append(head, p);
      breakdown.appendChild(card);
    });

    $('pest-disclaimer').textContent = res.disclaimer;
  }

  async function loadPestScans() {
    try {
      const data = await apiFetch('/api/pest/scans');
      const wrap = $('pest-scans-list');
      if (!wrap) return;
      wrap.replaceChildren();
      if (!data.scans || !data.scans.length) {
        const p = document.createElement('p');
        p.className = 'muted-text';
        p.textContent = 'No camera or photo scans saved yet.';
        wrap.appendChild(p);
        return;
      }
      data.scans.forEach((s) => {
        const row = document.createElement('div');
        row.className = 'recent-row';
        const left = document.createElement('div');
        const t = document.createElement('strong');
        t.textContent = `${s.predicted_label} (${s.confidence_pct}%)`;
        const sub = document.createElement('small');
        sub.textContent = `${s.category} · ${s.date} · ${s.model_used}`;
        left.append(t, sub);
        const del = document.createElement('button');
        del.type = 'button';
        del.className = 'btn-danger-outline btn-xs';
        del.textContent = 'Delete';
        del.addEventListener('click', async () => {
          await apiFetch(`/api/pest/scans/${s.id}`, { method: 'DELETE' });
          loadPestScans();
        });
        row.append(left, del);
        wrap.appendChild(row);
      });
    } catch {
      // Non-fatal
    }
  }

  async function loadPestGuide(q = '') {
    try {
      const data = await apiFetch(`/api/pest/guide?q=${encodeURIComponent(q)}`);
      const list = $('pest-guide-list');
      if (!list) return;
      list.replaceChildren();
      (data.items || []).forEach((item) => {
        const div = document.createElement('div');
        div.className = 'tip-row';
        const t = document.createElement('strong');
        t.textContent = `${item.category} (${item.severity})`;
        const p = document.createElement('p');
        p.textContent = `${item.summary} Examples: ${item.examples}. ${item.pesticide_class}`;
        div.append(t, p);
        list.appendChild(div);
      });
    } catch {
      // Non-fatal
    }
  }

  // ==========================================
  // FARM PLANNER: LEAFLET MAP, TASKS & CALCULATORS
  // ==========================================

  let farmMap = null;
  let farmLayerGroup = null;

  function renderFarmMap() {
    const mapDiv = $('farm-map');
    const listWrap = $('fp-map-plots-list');
    if (listWrap) {
      listWrap.replaceChildren();
      if (!state.plots.length) {
        const p = document.createElement('p');
        p.className = 'muted-text';
        p.textContent = 'No field plots yet. Click "+ Add / Manage Plots" or click the map to pin your first plot.';
        listWrap.appendChild(p);
      } else {
        state.plots.forEach((plot) => {
          const row = document.createElement('div');
          row.className = 'recent-row';
          const left = document.createElement('div');
          const strong = document.createElement('strong');
          strong.textContent = `${plot.name} (${plot.soil_type})`;
          const small = document.createElement('small');
          const coordTxt = plot.latitude !== null && plot.longitude !== null
            ? `${plot.latitude.toFixed(4)}, ${plot.longitude.toFixed(4)}`
            : 'No GPS pin';
          const scoreTxt = plot.latest_score !== null && plot.latest_score !== undefined
            ? `Match ${plot.latest_score}/100 (${plot.latest_crop || ''})`
            : 'No analysis yet';
          small.textContent = `${coordTxt} · ${scoreTxt}`;
          left.append(strong, small);

          const acts = document.createElement('div');
          acts.className = 'table-actions';
          if (plot.latitude !== null && plot.longitude !== null) {
            const wBtn = document.createElement('button');
            wBtn.type = 'button';
            wBtn.className = 'btn-outline btn-xs';
            wBtn.textContent = 'Plot Weather';
            wBtn.addEventListener('click', async () => {
              navigateTo('weather');
              const data = await apiFetch(
                `/api/weather?city=${encodeURIComponent(plot.location || plot.name)}&lat=${plot.latitude}&lon=${plot.longitude}`
              );
              state.weatherData = data;
              state.weatherLoaded = true;
              renderWeatherData(data);
            });
            acts.appendChild(wBtn);
          }
          row.append(left, acts);
          listWrap.appendChild(row);
        });
      }
    }

    if (!mapDiv) return;
    if (typeof window.L === 'undefined') {
      mapDiv.innerHTML = '<div style="padding:24px;text-align:center;color:#5C6F62;">Map tiles require internet access (Leaflet CDN unavailable offline). Your GPS plots still work in the list on the right.</div>';
      return;
    }

    if (!farmMap) {
      farmMap = window.L.map('farm-map').setView([15.3173, 75.7139], 5);
      window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18,
      }).addTo(farmMap);
      farmLayerGroup = window.L.layerGroup().addTo(farmMap);

      farmMap.on('click', (e) => {
        const lat = e.latlng.lat.toFixed(6);
        const lon = e.latlng.lng.toFixed(6);
        if ($('plot-lat-input')) $('plot-lat-input').value = lat;
        if ($('plot-lon-input')) $('plot-lon-input').value = lon;
        if ($('map-status-pill')) $('map-status-pill').textContent = `PINNED: ${lat}, ${lon}`;
        openPlotsModal();
        showToast(`Selected coordinates (${lat}, ${lon}) for new plot.`, 'info');
      });
    }

    setTimeout(() => farmMap.invalidateSize(), 150);
    farmLayerGroup.clearLayers();
    const coords = [];
    state.plots.forEach((plot) => {
      if (plot.latitude === null || plot.longitude === null) return;
      const color = plot.latest_score === null || plot.latest_score === undefined
        ? '#2B6CB0'
        : plot.latest_score >= 75
          ? '#247A49'
          : plot.latest_score >= 55
            ? '#D98A1E'
            : '#B42318';
      const marker = window.L.circleMarker([plot.latitude, plot.longitude], {
        radius: 9,
        color: '#123B26',
        weight: 2,
        fillColor: color,
        fillOpacity: 0.9,
      });
      marker.bindPopup(
        `<strong>${plot.name}</strong><br>Soil: ${plot.soil_type}<br>` +
        (plot.latest_score !== null && plot.latest_score !== undefined
          ? `Latest Match: ${plot.latest_score}/100 (${plot.latest_fertilizer})`
          : 'No analysis yet')
      );
      marker.addTo(farmLayerGroup);
      coords.push([plot.latitude, plot.longitude]);
    });
    if (coords.length) {
      farmMap.fitBounds(coords, { padding: [30, 30], maxZoom: 12 });
    }
  }

  async function loadTasks() {
    try {
      const status = $('task-filter-status')?.value || 'all';
      const data = await apiFetch(`/api/tasks?status=${encodeURIComponent(status)}`);
      const wrap = $('tasks-list-wrap');
      if (!wrap) return;
      wrap.replaceChildren();
      if (!data.tasks || !data.tasks.length) {
        const p = document.createElement('p');
        p.className = 'muted-text';
        p.textContent = 'No tasks in this filter yet. Add a seasonal scouting or irrigation reminder.';
        wrap.appendChild(p);
        return;
      }
      data.tasks.forEach((task) => {
        const row = document.createElement('div');
        row.className = `recent-row${task.completed ? ' task-row-done' : ''}`;
        const left = document.createElement('div');
        const t = document.createElement('strong');
        t.textContent = task.title;
        const sub = document.createElement('small');
        sub.textContent = `${task.category}${task.plot_name ? ` · ${task.plot_name}` : ''}${task.due_date ? ` · Due ${task.due_date}` : ''}`;
        left.append(t, sub);

        const acts = document.createElement('div');
        acts.className = 'table-actions';
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = task.completed ? 'btn-outline btn-xs' : 'btn-primary btn-xs';
        toggleBtn.textContent = task.completed ? 'Reopen' : 'Done ✓';
        toggleBtn.addEventListener('click', async () => {
          await apiFetch(`/api/tasks/${task.id}`, { method: 'PATCH', body: JSON.stringify({}) });
          loadTasks();
        });

        const delBtn = document.createElement('button');
        delBtn.type = 'button';
        delBtn.className = 'btn-danger-outline btn-xs';
        delBtn.textContent = 'Delete';
        delBtn.addEventListener('click', async () => {
          await apiFetch(`/api/tasks/${task.id}`, { method: 'DELETE' });
          loadTasks();
        });

        acts.append(toggleBtn, delBtn);
        row.append(left, acts);
        wrap.appendChild(row);
      });
    } catch {
      // Non-fatal
    }
  }

  function updateCalculators() {
    // 1. Area Converter
    const val = Math.max(0, Number($('calc-area-val')?.value || 0));
    const unit = $('calc-area-unit')?.value || 'acre';
    const toSqm = { acre: 4046.8564, hectare: 10000, sqm: 1, guntha: 101.1714 };
    const sqm = val * (toSqm[unit] || 4046.8564);
    if ($('calc-area-out')) {
      $('calc-area-out').textContent =
        `${(sqm / 4046.8564).toFixed(3)} Acres | ${(sqm / 10000).toFixed(3)} Hectares | ` +
        `${Math.round(sqm).toLocaleString()} m² | ${(sqm / 101.1714).toFixed(2)} Guntha`;
    }

    // 2. Plant Population
    const popAcres = Math.max(0.01, Number($('calc-pop-acres')?.value || 1));
    const rowCm = Math.max(1, Number($('calc-row-cm')?.value || 45));
    const plantCm = Math.max(1, Number($('calc-plant-cm')?.value || 15));
    const areaSqm = popAcres * 4046.8564;
    const perPlantSqm = (rowCm / 100) * (plantCm / 100);
    const estPlants = Math.round(areaSqm / perPlantSqm);
    if ($('calc-pop-out')) {
      $('calc-pop-out').textContent = `Estimated Population: ${estPlants.toLocaleString()} plants (${Math.round(1 / perPlantSqm)} plants/m²)`;
    }

    // 3. Irrigation Water Volume
    const irrAcres = Math.max(0.01, Number($('calc-irr-acres')?.value || 1));
    const irrMm = Math.max(1, Number($('calc-irr-mm')?.value || 25));
    const cubicMeters = (irrAcres * 4046.8564) * (irrMm / 1000);
    const liters = Math.round(cubicMeters * 1000);
    if ($('calc-irr-out')) {
      $('calc-irr-out').textContent = `Volume Needed: ${liters.toLocaleString()} Liters (${cubicMeters.toFixed(1)} m³)`;
    }
  }

  function setupFarmPlanner() {
    $('task-create-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        await apiFetch('/api/tasks', {
          method: 'POST',
          body: JSON.stringify({
            title: $('task-title').value.trim(),
            category: $('task-category').value,
            plot_id: $('task-plot-id').value,
            due_date: $('task-due').value,
          }),
        });
        $('task-create-form').reset();
        showToast('Field task added.', 'success');
        loadTasks();
      } catch (err) {
        showToast(err.message, 'error');
      }
    });

    $('task-filter-status')?.addEventListener('change', loadTasks);

    ['calc-area-val', 'calc-area-unit', 'calc-pop-acres', 'calc-row-cm', 'calc-plant-cm', 'calc-irr-acres', 'calc-irr-mm']
      .forEach((id) => {
        $(id)?.addEventListener('input', updateCalculators);
        $(id)?.addEventListener('change', updateCalculators);
      });

    document.querySelectorAll('.seg-tabs[data-tab-group="farm-planner"] .seg-tab').forEach((btn) => {
      btn.addEventListener('click', () => {
        if (btn.dataset.tabTarget === 'fp-tab-map') {
          setTimeout(() => farmMap && farmMap.invalidateSize(), 120);
        }
      });
    });

    updateCalculators();
  }

  // ==========================================
  // INITIALIZE
  // ==========================================

  document.addEventListener('DOMContentLoaded', async () => {
    applyThemeAndUnits();
    applyLanguage(state.lang);
    setupNavigation();
    setupAuthAndSettings();
    setupPlotsModal();
    setupSoilAnalysis();
    setupCropRecommendation();
    setupPestCamera();
    setupFarmPlanner();
    setupFertilizerGuide();
    setupWeather();
    setupChatbot();
    setupHistoryView();

    await refreshSession();
    await loadPlots();
    await loadDashboard();
  });
})();
