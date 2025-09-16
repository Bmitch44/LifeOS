"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

export type SnaptradeAccount = any

export type SnaptradeAccountCreate = {
  clerk_user_id: string
  account_id: string
  connection_id: string
  name: string
  number: string
  institution_name: string
  status: string
  type: string
  current_balance: number
  currency: string
}

export type SnaptradeAccountUpdate = SnaptradeAccountCreate

export function useGetSnaptradeAccount(id: number, refresh: boolean = false, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["snaptrade-account", id, refresh],
    queryFn: async () => {
      const token = await getToken()
      const qs = refresh ? "?refresh=true" : ""
      return api.getJson<SnaptradeAccount>(`/v1/snaptrade/accounts/${id}${qs}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled,
  })
}

export function useCreateSnaptradeAccount() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: SnaptradeAccountCreate) => {
      const token = await getToken()
      return api.postJson<SnaptradeAccount>(`/v1/snaptrade/accounts`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["snaptrade-account"] }),
  })
}

export function useUpdateSnaptradeAccount() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number; body: SnaptradeAccountUpdate }) => {
      const token = await getToken()
      return api.putJson<SnaptradeAccount>(`/v1/snaptrade/accounts/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: (_data, variables) => {
      qc.invalidateQueries({ queryKey: ["snaptrade-account", variables.id] })
    },
  })
}

export function useDeleteSnaptradeAccount() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson<{ message: string }>(`/v1/snaptrade/accounts/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["snaptrade-account"] }),
  })
}

export function useSyncSnaptradeAccounts() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async () => {
      const token = await getToken()
      return api.getJson<{ message: string }>(`/v1/snaptrade/accounts/sync`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["snaptrade-account"] }),
  })
}


