"use client"

import { User } from "@/src/core/api/generated/types"
import { useDeleteUser } from "@/src/features/users/hooks/useUsers"
import { WarningDialog } from "@/components/dialogs/WarningDialog"
import { Card, CardHeader, CardTitle, CardContent } from "@workspace/ui/components/card"
import { UserFormDialog } from "@/src/features/users/components/UserFormDialog"


export function UserCard({ user }: { user: User }) {
  const { mutate: deleteUser } = useDeleteUser()
  return (
    <Card>
      <CardHeader>
        <CardTitle>{user.email}</CardTitle>
      </CardHeader>
      <CardContent>
        <UserFormDialog id={user.id!} edit={true} />
        <WarningDialog 
            title="Delete User"
            description="Are you sure you want to delete this user?"
            onConfirm={() => deleteUser(user.id!)}
        />
      </CardContent>
    </Card>
  )
}