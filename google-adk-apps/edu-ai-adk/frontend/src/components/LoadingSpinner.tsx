export default function LoadingSpinner({
  message = "Carregando...",
}: {
  message?: string;
}) {
  return (
    <div className="flex h-screen items-center justify-center essay-section-background relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-enem-deep-purple/20 to-enem-purple/20 z-0" />
      <div className="absolute -top-40 -right-40 w-80 h-80 bg-enem-purple/20 rounded-full blur-3xl" />
      <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-enem-deep-purple/20 rounded-full blur-3xl" />

      <div className="flex flex-col items-center space-y-4 relative z-10">
        <div className="relative">
          <div className="absolute inset-0 rounded-full bg-gradient-to-r from-enem-purple to-enem-deep-purple opacity-50 blur-md"></div>
          <div className="h-12 w-12 animate-spin rounded-full border-b-2 border-primary relative"></div>
        </div>
        <p className="text-lg text-white">Loading...</p>
      </div>
    </div>
  );
}
