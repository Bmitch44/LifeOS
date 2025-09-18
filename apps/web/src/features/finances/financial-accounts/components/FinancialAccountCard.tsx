import { FinancialAccount } from "@/src/core/api/generated/types";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@workspace/ui/components/card";
import { Badge } from "@workspace/ui/components/badge";


export function FinancialAccountCard({ financialAccount }: { financialAccount: FinancialAccount }) {
  return (
      <Card className="flex flex-col justify-between">
        <CardHeader>
          <div className="flex items-center justify-between gap-2">
            <CardTitle>{financialAccount.name}</CardTitle>
            <Badge variant="outline">{financialAccount.source} | {financialAccount.type}</Badge>
          </div>
          <CardDescription>{financialAccount.institution_name}</CardDescription>
        </CardHeader>
        <CardContent>
          <p>${financialAccount.current_balance} {financialAccount.currency}</p>
        </CardContent>
      </Card>
  );
}