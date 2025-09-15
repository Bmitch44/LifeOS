"use client"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

export function useAllDocuments(page = 1, size = 20) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["documents", page, size],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson(`/v1/documents?page=${page}&size=${size}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    staleTime: 30_000,
  })
}

export function useGetDocument(id: number, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["documents", id],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson(`/v1/documents/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled,
  })
}

export function useCreateDocument() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: any) => {
      const token = await getToken()
      return api.postJson(`/v1/documents`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["documents"] }),
  })
}

export function useUpdateDocument() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number; body: any }) => {
      const token = await getToken()
      return api.putJson(`/v1/documents/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["documents"] }),
  })
}

export function useDeleteDocument() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson(`/v1/documents/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["documents"] }),
  })
}

