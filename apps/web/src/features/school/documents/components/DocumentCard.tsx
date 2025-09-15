"use client"

import { WarningDialog } from "@/components/dialogs/WarningDialog"
import { Card, CardHeader, CardTitle, CardContent } from "@workspace/ui/components/card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@workspace/ui/components/dropdown-menu"
import { Button } from "@workspace/ui/components/button"
import { MoreHorizontal, FileText } from "lucide-react"
import { Badge } from "@workspace/ui/components/badge"
import { useState } from "react"
import { DocumentFormDialog } from "./DocumentFormDialog"
import { useDeleteDocument } from "../hooks/useDocuments"


export function DocumentCard({ document }: { document: any }) {
  const { mutate: deleteDocument } = useDeleteDocument()
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [editOpen, setEditOpen] = useState(false)

  const handleDelete = () => {
    deleteDocument(document.id!)
    setDeleteOpen(false)
  }

  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <Badge className="bg-muted text-foreground/80">{document.file_type || "file"}</Badge>
            </div>
            <CardTitle className="mt-1 truncate text-base sm:text-lg">{document.name}</CardTitle>
          </div>

          <div className="flex items-start gap-2">
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
          </div>
        </div>
      </CardHeader>
      <CardContent className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
        <div className="flex items-center gap-2 text-muted-foreground">
          <FileText className="h-4 w-4" />
          <a className="truncate text-primary" href={document.file_url} target="_blank" rel="noreferrer">Open</a>
        </div>
        {document.description ? (
          <p className="col-span-1 sm:col-span-2 text-foreground/80">{document.description}</p>
        ) : null}

        <DocumentFormDialog id={document.id!} edit={true} open={editOpen} setOpen={setEditOpen} />
        <WarningDialog
          title="Delete Document"
          description="Are you sure you want to delete this document?"
          onConfirm={handleDelete}
          open={deleteOpen}
          setOpen={setDeleteOpen}
        />
      </CardContent>
    </Card>
  )
}

