"use client"

import { z } from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@workspace/ui/components/form"
import { Input } from "@workspace/ui/components/input"
import { useGetUser, useUpdateUser } from "../hooks/useUsers"
import { Button } from "@workspace/ui/components/button"

const formSchema = z.object({
    email: z.string().email(),
})

export function UserForm({ id, edit }: { id: number, edit: boolean }) {
    const { data: user, isPending } = useGetUser(id, edit)
    const { mutate: updateUser } = useUpdateUser()


    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: "",
        },
    })
    
    const onSubmit = (data: z.infer<typeof formSchema>) => {
        if (edit) {
            updateUser({ id, body: { email: data.email } })
        }
    }
    
    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)}>
                <FormField control={form.control} name="email" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Email</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <Button type="submit">Submit</Button>
            </form>
        </Form>
    )
}