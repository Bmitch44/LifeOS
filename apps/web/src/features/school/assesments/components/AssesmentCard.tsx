"use client"

import { Assesment } from "@/src/core/api/generated/types"
import { Card, CardHeader, CardTitle, CardContent } from "@workspace/ui/components/card"
import { AssesmentFormDialog } from "@/src/features/school/assesments/components/AssesmentFormDialog"
import { useState } from "react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@workspace/ui/components/dropdown-menu"
import { Button } from "@workspace/ui/components/button"
import { MoreHorizontal } from "lucide-react"
import { WarningDialog } from "@/components/dialogs/WarningDialog"
import { useDeleteAssesment } from "@/src/features/school/assesments/hooks/useAssesments"

export function AssesmentCard({ assesment }: { assesment: Assesment }) {
  const { mutate: deleteAssesment } = useDeleteAssesment()
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [editOpen, setEditOpen] = useState(false)

  const handleDelete = () => {
    deleteAssesment(assesment.id!)
    setDeleteOpen(false)
  }
  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center w-full">
          <CardTitle>{assesment.name}</CardTitle>
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
          </DropdownMenu>
          <AssesmentFormDialog id={assesment.id!} edit={true} open={editOpen} setOpen={setEditOpen} />
          <WarningDialog
            title="Delete Assesment"
            description="Are you sure you want to delete this assesment?"
            onConfirm={handleDelete}
            open={deleteOpen}
            setOpen={setDeleteOpen}
          />
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col gap-2">
          <p>{assesment.description}</p>
        </div>
      </CardContent>
    </Card>
  )
}