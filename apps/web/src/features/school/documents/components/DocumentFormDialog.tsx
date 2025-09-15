import { DocumentForm } from "./DocumentForm"
import { Button } from "@workspace/ui/components/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@workspace/ui/components/dialog"

export function DocumentFormDialog({ id, edit, open, setOpen }: { id: number, edit: boolean, open: boolean, setOpen: (open: boolean) => void }) {
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      {!edit && (
        <DialogTrigger asChild>
          <Button onClick={() => setOpen(true)}>{edit ? "Edit Document" : "Add Document"}</Button>
        </DialogTrigger>
      )}
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{edit ? "Edit Document" : "Add Document"}</DialogTitle>
        </DialogHeader>
        <DocumentForm id={id} edit={edit} setOpen={setOpen} />
      </DialogContent>
    </Dialog>
  )
}

