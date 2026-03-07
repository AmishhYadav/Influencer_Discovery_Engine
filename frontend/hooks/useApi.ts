import useSWR from 'swr';
import { SearchQuery, SearchResponse, Creator } from '@/lib/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const fetcher = async (url: string) => {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`API Error: ${res.status}`);
  }
  return res.json();
};

export function useSearch(query: SearchQuery | null) {
  const queryString = query
    ? new URLSearchParams(
        Object.entries(query).reduce((acc, [key, value]) => {
          if (Array.isArray(value)) {
            acc[key] = value.join(',');
          } else if (value !== undefined && value !== null) {
            acc[key] = String(value);
          }
          return acc;
        }, {} as Record<string, string>)
      ).toString()
    : null;

  const { data, error, isLoading } = useSWR<SearchResponse>(
    query ? `${API_BASE_URL}/api/search?${queryString}` : null,
    fetcher,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
    }
  );

  return {
    results: data,
    isLoading,
    error,
  };
}

export function useCreator(creatorId: string | null) {
  const { data, error, isLoading } = useSWR(
    creatorId ? `${API_BASE_URL}/api/creators/${creatorId}` : null,
    fetcher,
    {
      revalidateOnFocus: false,
    }
  );

  return {
    creator: data,
    isLoading,
    error,
  };
}

export function useCreators(page = 1, perPage = 20) {
  const { data, error, isLoading } = useSWR(
    `${API_BASE_URL}/api/creators?page=${page}&per_page=${perPage}`,
    fetcher,
    {
      revalidateOnFocus: false,
    }
  );

  return {
    creators: data,
    isLoading,
    error,
  };
}

export function useFilterOptions() {
  const { data, error, isLoading } = useSWR(
    `${API_BASE_URL}/api/filter-options`,
    fetcher,
    {
      revalidateOnFocus: false,
      dedupingInterval: 3600000, // Cache for 1 hour
    }
  );

  return {
    filterOptions: data,
    isLoading,
    error,
  };
}
