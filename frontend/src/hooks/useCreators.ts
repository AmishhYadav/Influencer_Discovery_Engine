import { useQuery, useMutation } from '@tanstack/react-query'
import {
    fetchCreators,
    fetchCreator,
    generateBriefing,
    fetchBriefing,
    fetchMultiCreators,
    fetchMultiCreator,
} from '@/api/client'
import type { Platform } from '@/api/client'

export function useCreators(params: { limit?: number; offset?: number; minScore?: number | null }) {
    return useQuery({
        queryKey: ['creators', params],
        queryFn: () => fetchCreators(params),
    })
}

export function useCreator(id: string | null) {
    return useQuery({
        queryKey: ['creator', id],
        queryFn: () => fetchCreator(id!),
        enabled: !!id,
    })
}

export function useMultiCreators(params: {
    limit?: number
    offset?: number
    platform?: Platform | null
    minScore?: number | null
}) {
    return useQuery({
        queryKey: ['multiCreators', params],
        queryFn: () => fetchMultiCreators(params),
    })
}

export function useMultiCreator(id: string | null) {
    return useQuery({
        queryKey: ['multiCreator', id],
        queryFn: () => fetchMultiCreator(id!),
        enabled: !!id,
    })
}

export function useGenerateBriefing() {
    return useMutation({
        mutationFn: (params: { channel_id: string; campaign_context?: string }) =>
            generateBriefing(params),
    })
}

export function useBriefingPolling(briefingId: string | null) {
    return useQuery({
        queryKey: ['briefing', briefingId],
        queryFn: () => fetchBriefing(briefingId!),
        enabled: !!briefingId,
        refetchInterval: (query) => {
            const data = query.state.data
            if (data && (data.status === 'completed' || data.status === 'failed')) {
                return false
            }
            return 3000
        },
    })
}
