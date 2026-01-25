import CenteredFlow from "../../ux/layouts/CenteredFlow";
import Button from "../../ux/components/common/Button";
import { colors } from "../../ux/tokens/colors";

function PricingCard({
  title,
  price,
  description,
  highlight,
}: {
  title: string;
  price: string;
  description: string[];
  highlight?: boolean;
}) {
  return (
    <div
      style={{
        border: highlight
          ? `1px solid ${colors.accent}`
          : "1px solid #2A2F3A",
        padding: 32,
        borderRadius: 6,
        background: colors.bgSecondary,
      }}
    >
      <h3 style={{ color: colors.textPrimary }}>{title}</h3>
      <p style={{ color: colors.textPrimary, fontSize: 24, marginTop: 8 }}>
        {price}
      </p>

      <ul style={{ color: colors.textMuted, marginTop: 16 }}>
        {description.map((d) => (
          <li key={d} style={{ marginBottom: 8 }}>
            {d}
          </li>
        ))}
      </ul>

      <div style={{ marginTop: 24 }}>
        <Button>Select</Button>
      </div>
    </div>
  );
}

export default function PricingPage() {
  return (
    <CenteredFlow>
      <h1 style={{ color: colors.textPrimary }}>Choose Your Review</h1>

      <p style={{ color: colors.textMuted, marginTop: 16 }}>
        Each submission is evaluated through a selective, multi-stage
        quality system. Only suitable images proceed.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: 24,
          marginTop: 48,
        }}
      >
        <PricingCard
          title="Essential"
          price="$49"
          description={[
            "Selective image review",
            "Pass / Not Suitable decision",
            "Final approval remains yours",
          ]}
        />

        <PricingCard
          title="Curated"
          price="$149"
          highlight
          description={[
            "Expanded review criteria",
            "Correctable images identified",
            "Identity-preserving selection",
          ]}
        />

        <PricingCard
          title="Studio"
          price="$349"
          description={[
            "Priority evaluation",
            "Iterative refinement support",
            "Best results for modeling",
          ]}
        />
      </div>
    </CenteredFlow>
  );
}
