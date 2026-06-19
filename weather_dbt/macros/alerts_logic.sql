{%- macro generate_weather_alert(temp_max_col, temp_min_col, precip_col) -%}
  case
    when {{ temp_max_col }} > 35 then 'HEATWAVE'
    when {{ temp_min_col }} < 10 then 'COLD_WAVE'
    when {{ precip_col }} > 20 then 'HEAVY_RAIN'
    else 'None'
  end
{%- endmacro -%}

{%- macro get_alert_severity(temp_max_col, temp_min_col, precip_col) -%}
  case
    when {{ temp_max_col }} > 40 then 'CRITICAL'
    when {{ temp_max_col }} > 35 then 'WARNING'
    when {{ temp_min_col }} < 0 then 'CRITICAL'
    when {{ temp_min_col }} < 10 then 'WARNING'
    when {{ precip_col }} > 40 then 'CRITICAL'
    when {{ precip_col }} > 20 then 'WARNING'
    else 'LOW'
  end
{%- endmacro -%}
