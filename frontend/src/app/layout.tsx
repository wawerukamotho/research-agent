import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Providers from "@/components/Providers";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Deep Research Agent",
  description: "Autonomous AI Research Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Providers>
          <div className="min-h-screen bg-slate-50">
            <header className="bg-white border-b px-6 py-4">
              <h1 className="text-xl font-bold text-slate-900">Deep Research Agent</h1>
            </header>
            <main className="container mx-auto py-8 px-4">
              {children}
            </main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
