"use client"

import { User } from "@/src/core/api/generated/types"
import { useDeleteUser } from "@/src/features/users/hooks/useUsers"
import { WarningDialog } from "@/components/dialogs/WarningDialog"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@workspace/ui/components/card"
import { UserFormDialog } from "@/src/features/users/components/UserFormDialog"
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@workspace/ui/components/dropdown-menu"
import { Button } from "@workspace/ui/components/button"
import { MoreHorizontal } from "lucide-react"
import { useState } from "react"



export function UserCard({ user }: { user: User }) {
  const { mutate: deleteUser } = useDeleteUser()
  const [editOpen, setEditOpen] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)

  const handleDelete = () => {
    deleteUser(user.id!)
    setDeleteOpen(false)
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center w-full">
          <CardTitle>{user.first_name} {user.last_name}</CardTitle>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="hover:bg-muted/60">
                    <MoreHorizontal className="h-4 w-4" />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setEditOpen(true)}>Edit</DropdownMenuItem>
                <DropdownMenuItem className="text-destructive" onClick={() => setDeleteOpen(true)}>Delete</DropdownMenuItem>
            </DropdownMenuContent>
            <UserFormDialog id={user.id!} edit={true} open={editOpen} setOpen={setEditOpen} />
            <WarningDialog 
                title="Delete User"
                description="Are you sure you want to delete this user?"
                onConfirm={handleDelete}
                open={deleteOpen}
                setOpen={setDeleteOpen}
            />
          </DropdownMenu>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col gap-2">
          <p>{user.email}</p>
          <p>{user.phone}</p>
        </div>
      </CardContent>
    </Card>
  )
}