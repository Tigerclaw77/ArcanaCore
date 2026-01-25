import { colors } from "../tokens/colors";
import { spacing } from "../tokens/spacing";

export default function CenteredFlow({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: colors.bgPrimary,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: spacing.xl,
      }}
    >
      <div style={{ maxWidth: 720, width: "100%" }}>
        {children}
      </div>
    </div>
  );
}
