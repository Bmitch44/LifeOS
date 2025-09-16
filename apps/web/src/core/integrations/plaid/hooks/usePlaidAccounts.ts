"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

export type PlaidAccount = any

export type PlaidAccountCreate = {
  clerk_user_id: string
  account_id: string
  name: string
  official_name: string
  type: string
  subtype: string
  current_balance: number
  available_balance: number
  iso_currency_code: string
  mask: string
}

export type PlaidAccountUpdate = PlaidAccountCreate

export function useGetPlaidAccount(id: number, refresh: boolean = false, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["plaid-account", id, refresh],
    queryFn: async () => {
      const token = await getToken()
      const qs = refresh ? "?refresh=true" : ""
      return api.getJson<PlaidAccount>(`/v1/plaid/accounts/${id}${qs}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled,
  })
}

export function useCreatePlaidAccount() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: PlaidAccountCreate) => {
      const token = await getToken()
      return api.postJson<PlaidAccount>(`/v1/plaid/accounts`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["plaid-account"] }),
  })
}

export function useUpdatePlaidAccount() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number; body: PlaidAccountUpdate }) => {
      const token = await getToken()
      return api.putJson<PlaidAccount>(`/v1/plaid/accounts/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: (_data, variables) => {
      qc.invalidateQueries({ queryKey: ["plaid-account", variables.id] })
    },
  })
}

export function useDeletePlaidAccount() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson<{ message: string }>(`/v1/plaid/accounts/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["plaid-account"] }),
  })
}

export function useSyncPlaidAccounts() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async () => {
      const token = await getToken()
      return api.getJson<{ message: string }>(`/v1/plaid/accounts/sync`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["plaid-account"] }),
  })
}


