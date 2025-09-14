import { UserForm } from "@/src/features/users/components/UserForm"
import { Button } from "@workspace/ui/components/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@workspace/ui/components/dialog"

export function UserFormDialog({ id, edit }: { id: number, edit: boolean }) {
    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button>{edit ? "Edit User" : "Add User"}</Button>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{edit ? "Edit User" : "Add User"}</DialogTitle>
                </DialogHeader>
                <UserForm id={id} edit={edit} />
            </DialogContent>
        </Dialog>
    )
}