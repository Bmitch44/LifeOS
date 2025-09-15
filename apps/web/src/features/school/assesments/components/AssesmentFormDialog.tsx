import { AssesmentForm } from "@/src/features/school/assesments/components/AssesmentForm"
import { Button } from "@workspace/ui/components/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@workspace/ui/components/dialog"

export function AssesmentFormDialog({ id, edit, open, setOpen }: { id: number, edit: boolean, open: boolean, setOpen: (open: boolean) => void }) {
    return (
        <Dialog open={open} onOpenChange={setOpen}>
            {!edit && (
                <DialogTrigger asChild>
                    <Button onClick={() => setOpen(true)}>{edit ? "Edit Assesment" : "Add Assesment"}</Button>
                </DialogTrigger>
            )}
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{edit ? "Edit Assesment" : "Add Assesment"}</DialogTitle>
                </DialogHeader>
                <AssesmentForm id={id} edit={edit} setOpen={setOpen} />
            </DialogContent>
        </Dialog>
    )
}