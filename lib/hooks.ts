'use client'

import { useState, useCallback, useEffect } from 'react'
import {
  searchCreators,
  getCreatorsByNiche,
  getCreatorDetail,
  getTrendingCreators,
  SearchParams,
  Creator,
  SearchResponse,
  CreatorDetailResponse,
} from './api'

export const useSearch = () => {
  const [results, setResults] = useState<Creator[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [totalResults, setTotalResults] = useState(0)

  const search = useCallback(async (params: SearchParams) => {
    setLoading(true)
    setError(null)
    try {
      const response: SearchResponse = await searchCreators(params)
      setResults(response.results)
      setTotalResults(response.total)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed')
      setResults([])
    } finally {
      setLoading(false)
    }
  }, [])

  return { results, loading, error, search, totalResults }
}

export const useCreatorsByNiche = (niche: string, enabled = true) => {
  const [creators, setCreators] = useState<Creator[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!enabled || !niche) return

    const fetchCreators = async () => {
      setLoading(true)
      setError(null)
      try {
        const data = await getCreatorsByNiche(niche)
        setCreators(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch creators')
        setCreators([])
      } finally {
        setLoading(false)
      }
    }

    fetchCreators()
  }, [niche, enabled])

  return { creators, loading, error }
}

export const useCreatorDetail = (creatorId: string) => {
  const [detail, setDetail] = useState<CreatorDetailResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!creatorId) return

    const fetchDetail = async () => {
      setLoading(true)
      setError(null)
      try {
        const data = await getCreatorDetail(creatorId)
        setDetail(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch creator details')
        setDetail(null)
      } finally {
        setLoading(false)
      }
    }

    fetchDetail()
  }, [creatorId])

  return { detail, loading, error }
}

export const useTrendingCreators = (limit = 10) => {
  const [creators, setCreators] = useState<Creator[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTrending = async () => {
      setLoading(true)
      setError(null)
      try {
        const data = await getTrendingCreators(limit)
        setCreators(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch trending creators')
        setCreators([])
      } finally {
        setLoading(false)
      }
    }

    fetchTrending()
  }, [limit])

  return { creators, loading, error }
}
