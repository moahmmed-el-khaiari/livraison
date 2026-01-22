import { Card, CardContent, Typography } from "@mui/material";

type Props = {
  title: string;
  value: number | string;
};

export default function StatCard({ title, value }: Props) {
  return (
    <Card
      variant="outlined"
      sx={{
        borderRadius: 3,
        height: "100%",
      }}
    >
      <CardContent>
        <Typography variant="overline" color="text.secondary">
          {title}
        </Typography>

        <Typography
          variant="h4"
          sx={{ fontWeight: 800, mt: 1 }}
        >
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}
