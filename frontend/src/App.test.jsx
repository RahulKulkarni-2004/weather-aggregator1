import { render, screen } from "@testing-library/react";
import App from "./App";

describe("Weather Aggregator", () => {
  test("renders the city input and Get Weather button", () => {
    render(<App />);

    expect(
      screen.getByPlaceholderText("Enter city")
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: "Get Weather" })
    ).toBeInTheDocument();
  });
});