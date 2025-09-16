"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

export type PlaidItem = any

export type PlaidItemCreate = {
  clerk_user_id: string
  item_id: string
  access_token: string
  institution_name: string
}

export type PlaidItemUpdate = PlaidItemCreate

export function useGetPlaidItem(id: number, refresh: boolean = false, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["plaid-item", id, refresh],
    queryFn: async () => {
      const token = await getToken()
      const qs = refresh ? "?refresh=true" : ""
      return api.getJson<PlaidItem>(`/v1/plaid/items/${id}${qs}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled,
  })
}

export function useCreatePlaidItem() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: PlaidItemCreate) => {
      const token = await getToken()
      return api.postJson<PlaidItem>(`/v1/plaid/items`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["plaid-item"] }),
  })
}

export function useUpdatePlaidItem() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number; body: PlaidItemUpdate }) => {
      const token = await getToken()
      return api.putJson<PlaidItem>(`/v1/plaid/items/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: (_data, variables) => {
      qc.invalidateQueries({ queryKey: ["plaid-item", variables.id] })
    },
  })
}

export function useDeletePlaidItem() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson<{ message: string }>(`/v1/plaid/items/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["plaid-item"] }),
  })
}

export function useSyncPlaidItems() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async () => {
      const token = await getToken()
      return api.getJson<{ message: string }>(`/v1/plaid/items/sync`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["plaid-item"] }),
  })
}


