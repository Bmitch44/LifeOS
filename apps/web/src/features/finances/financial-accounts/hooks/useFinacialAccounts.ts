"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"
import { FinancialAccountCreate, FinancialAccountUpdate, FinancialAccount, PaginatedFinancialAccounts } from "@/src/core/api/generated/types"

export function useAllFinancialAccounts(page = 1, size = 20) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["financial-accounts", page, size],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<PaginatedFinancialAccounts>(`/v1/finances/accounts?page=${page}&size=${size}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    staleTime: 30_000,
  })
}

export function useGetFinancialAccount(id: number, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["financial-account", id],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<FinancialAccount>(`/v1/finances/accounts/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled,
  })
}

export function useCreateFinancialAccount() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: FinancialAccountCreate) => {
      const token = await getToken()
      return api.postJson<FinancialAccount>(`/v1/finances/accounts`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["financial-account"] }),
  })
}

export function useUpdateFinancialAccount() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number; body: FinancialAccountUpdate }) => {
      const token = await getToken()
      return api.putJson<FinancialAccount>(`/v1/finances/accounts/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: (_data, variables) => {
      qc.invalidateQueries({ queryKey: ["financial-account", variables.id] })
    },
  })
}

export function useDeleteFinancialAccount() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson<{ message: string }>(`/v1/finances/accounts/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["financial-account"] }),
  })
}

export function useSyncFinancialAccounts() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async () => {
      const token = await getToken()
      return api.getJson<{ message: string }>(`/v1/finances/accounts/sync`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["financial-account"] }),
  })
}


