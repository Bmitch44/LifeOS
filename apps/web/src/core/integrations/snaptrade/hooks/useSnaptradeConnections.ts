"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

export type SnaptradeConnection = any

export type SnaptradeConnectionCreate = {
  clerk_user_id: string
  connection_id: string
  brokerage_name: string
}

export type SnaptradeConnectionUpdate = SnaptradeConnectionCreate

export function useGetSnaptradeConnection(id: number, refresh: boolean = false, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["snaptrade-connection", id, refresh],
    queryFn: async () => {
      const token = await getToken()
      const qs = refresh ? "?refresh=true" : ""
      return api.getJson<SnaptradeConnection>(`/v1/snaptrade/connections/${id}${qs}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled,
  })
}

export function useCreateSnaptradeConnection() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: SnaptradeConnectionCreate) => {
      const token = await getToken()
      return api.postJson<SnaptradeConnection>(`/v1/snaptrade/connections`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["snaptrade-connection"] }),
  })
}

export function useUpdateSnaptradeConnection() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number; body: SnaptradeConnectionUpdate }) => {
      const token = await getToken()
      return api.putJson<SnaptradeConnection>(`/v1/snaptrade/connections/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: (_data, variables) => {
      qc.invalidateQueries({ queryKey: ["snaptrade-connection", variables.id] })
    },
  })
}

export function useDeleteSnaptradeConnection() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson<{ message: string }>(`/v1/snaptrade/connections/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["snaptrade-connection"] }),
  })
}

export function useSyncSnaptradeConnections() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async () => {
      const token = await getToken()
      return api.getJson<{ message: string }>(`/v1/snaptrade/connections/sync`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["snaptrade-connection"] }),
  })
}


