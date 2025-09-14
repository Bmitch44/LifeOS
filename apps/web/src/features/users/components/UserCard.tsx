"use client"

import { UserOut } from "@/src/core/api/generated/types"
import { useDeleteUser } from "@/src/features/users/hooks/useUsers"
import { WarningDialog } from "@/components/dialogs/WarningDialog"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@workspace/ui/components/card"


export function UserCard({ user }: { user: UserOut }) {
  const { mutate: deleteUser } = useDeleteUser()
  return (
    <Card>
      <CardHeader>
        <CardTitle>{user.email}</CardTitle>
      </CardHeader>
      <CardContent>
        <WarningDialog 
            title="Delete User"
            description="Are you sure you want to delete this user?"
            onConfirm={() => deleteUser(user.id)}
        />
      </CardContent>
    </Card>
  )
}