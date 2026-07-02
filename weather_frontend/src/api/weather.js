import axios from 'axios'

const API = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// Cities
export const getCities = async () => {
  const { data } = await API.get('/cities')
  return data
}

// Weather Today
export const getWeatherToday = async (city = null) => {
  const params = city ? { city } : {}
  const { data } = await API.get('/weather/today', { params })
  return data
}

// Weather History
export const getWeatherHistory = async (city = null, dateFrom = null, dateTo = null) => {
  const params = {}
  if (city) params.city = city
  if (dateFrom) params.date_from = dateFrom
  if (dateTo) params.date_to = dateTo

  const { data } = await API.get('/weather/history', { params })
  return data
}

// Alerts
export const getAlerts = async (city = null) => {
  const params = city ? { city } : {}
  const { data } = await API.get('/weather/alerts', { params })
  return data
}

export const getAlertsSummary = async (city = null) => {
  const params = city ? { city } : {}
  const { data } = await API.get('/weather/alerts/summary', { params })
  return data
}