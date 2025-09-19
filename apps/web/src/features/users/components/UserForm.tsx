"use client"

import { z } from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@workspace/ui/components/form"
import { Input } from "@workspace/ui/components/input"
import { useGetUser, useUpdateUser } from "@/src/features/users/hooks/useUsers"
import { Button } from "@workspace/ui/components/button"
import { useEffect } from "react"

const formSchema = z.object({
    email: z.string().email(),
    first_name: z.string(),
    last_name: z.string(),
    phone: z.string(),
})

export function UserForm({ id, edit, setOpen }: { id: number, edit: boolean, setOpen: (open: boolean) => void }) {
    const { data: user, isPending } = useGetUser(id, edit)
    const { mutate: updateUser } = useUpdateUser()


    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: "",
            first_name: "",
            last_name: "",
            phone: "",
        },
    })

    useEffect(() => {
        if (edit && user) {
            form.reset({
                email: user.email ?? "",
                first_name: user.first_name ?? "",
                last_name: user.last_name ?? "",
                phone: user.phone ?? "",
            })
        }
    }, [edit, user, form])
    
    const onSubmit = (data: z.infer<typeof formSchema>) => {
        if (edit) {
            updateUser({ id, body: { email: data.email, first_name: data.first_name, last_name: data.last_name, phone: data.phone } })
            setOpen(false)
        }
    }
    
    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)}>
                <FormField control={form.control} name="email" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Email</FormLabel>
                        <FormControl>
                            <Input {...field} type="email" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="first_name" render={({ field }) => (
                    <FormItem>
                        <FormLabel>First Name</FormLabel>
                        <FormControl>
                            <Input {...field} type="text" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="last_name" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Last Name</FormLabel>
                        <FormControl>
                            <Input {...field} type="text" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="phone" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Phone</FormLabel>
                        <FormControl>
                            <Input {...field} type="tel" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <Button type="submit">Submit</Button>
            </form>
        </Form>
    )
}