"use client"
import { useUsers } from "../hooks/useUsers"

export function UserList() {
  const { data, isLoading, error } = useUsers()
  if (isLoading) return <div>Loading…</div>
  if (error) return <div>Failed to load users</div>
  return (
    <ul className="list-disc pl-4">
      {data?.items?.map((u: any) => (
        <li key={u.id}>{u.email}</li>
      ))}
    </ul>
  )
}


