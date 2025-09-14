import { UserForm } from "@/src/features/users/components/UserForm"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@workspace/ui/components/dialog"

export function UserFormDialog({ id, edit, open, setOpen }: { id: number, edit: boolean, open: boolean, setOpen: (open: boolean) => void }) {
    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{edit ? "Edit User" : "Add User"}</DialogTitle>
                </DialogHeader>
                <UserForm id={id} edit={edit} setOpen={setOpen} />
            </DialogContent>
        </Dialog>
    )
}