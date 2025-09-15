"use client"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { PaginatedAssesments, Assesment, AssesmentCreate, AssesmentUpdate } from "@/src/core/api/generated/types"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

export function useAllAssesments(page = 1, size = 20) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["assesments", page, size],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<PaginatedAssesments>(`/v1/assesments?page=${page}&size=${size}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    staleTime: 30_000,
  })
}

export function useGetAssesment(id: number, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["assesments", id],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<Assesment>(`/v1/assesments/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled,
  })
}

export function useCreateAssesment() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: AssesmentCreate) => {
      const token = await getToken()
      return api.postJson<Assesment>(`/v1/assesments`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["assesments"] }),
  })
}

export function useUpdateAssesment() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number, body: AssesmentUpdate }) => {
      const token = await getToken()
      return api.putJson<Assesment>(`/v1/assesments/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["assesments"] }),
  })
}

export function useDeleteAssesment() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson<{message: string}>(`/v1/assesments/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["assesments"] }),
  })
}