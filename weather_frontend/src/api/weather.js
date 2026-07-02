import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000
})

// ─── Cities ───
export const getCities = async () => {
  const { data } = await API.get('/cities')
  return data
}

// ─── Weather Today ───
export const getWeatherToday = async (city = null) => {
  const params = city ? { city } : {}
  const { data } = await API.get('/weather/today', { params })
  return data
}

// ─── Weather History ───
export const getWeatherHistory = async (city = null, dateFrom = null, dateTo = null) => {
  const params = {}
  if (city)     params.city      = city
  if (dateFrom) params.date_from = dateFrom
  if (dateTo)   params.date_to   = dateTo
  const { data } = await API.get('/weather/history', { params })
  return data
}

// ─── Analytics ───
export const getAnalyticsKpi = async (city = null) => {
  const params = city ? { city } : {}
  const { data } = await API.get('/analytics/kpi', { params })
  return data
}

export const getAnalyticsComparison = async () => {
  const { data } = await API.get('/analytics/comparison')
  return data
}

// ─── Alerts ───
export const getAlerts = async (city = null) => {
  const params = city ? { city } : {}
  const { data } = await API.get('/alerts', { params })
  return data
}

export const getAlertsSummary = async () => {
  const { data } = await API.get('/alerts/summary')
  return data
}