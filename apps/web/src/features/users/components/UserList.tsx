"use client"
import { useAllUsers } from "@/src/features/users/hooks/useUsers"
import { User } from "@/src/core/api/generated/types"
import { UserCard } from "@/src/features/users/components/UserCard"


export function UserList() {
  const { data, isLoading, error } = useAllUsers()
  if (isLoading) return <div>Loading…</div>
  if (error) return <div>Failed to load users</div>
  return (
    <div className="flex flex-col gap-4"> 
      <h1 className="text-xl font-bold">Users</h1>
      {data?.items?.map((user: User) => (
        <div key={user.id} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <UserCard user={user} />
        </div>
      ))}
    </div>
  )
}


