import { createClient } from "@supabase/supabase-js";

const MAX_CACHE_SIZE = 500;

function getSupabase() {
  return createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!
  );
}

export async function getCachedHint(cacheKey: string): Promise<string | null> {
  try {
    const supabase = getSupabase();
    const { data } = await supabase
      .from("econoquest_hint_cache")
      .select("hint, hits")
      .eq("cache_key", cacheKey)
      .single();

    if (!data) return null;

    // update last_used + hits in background
    (supabase
      .from("econoquest_hint_cache")
      .update({ last_used: new Date().toISOString(), hits: (data.hits ?? 1) + 1 })
      .eq("cache_key", cacheKey) as any)
      .catch(() => {});

    return data.hint as string;
  } catch {
    return null;
  }
}

export async function setCachedHint(
  cacheKey:      string,
  hint:          string,
  stateSnapshot: Record<string, unknown>
): Promise<void> {
  try {
    const supabase = getSupabase();

    // check size — evict LRU if over limit
    const { count } = await supabase
      .from("econoquest_hint_cache")
      .select("*", { count: "exact", head: true });

    if ((count ?? 0) >= MAX_CACHE_SIZE) {
      const { data: oldest } = await supabase
        .from("econoquest_hint_cache")
        .select("cache_key")
        .order("last_used", { ascending: true })
        .limit(1)
        .single();

      if (oldest) {
        await supabase
          .from("econoquest_hint_cache")
          .delete()
          .eq("cache_key", oldest.cache_key);
      }
    }

    await supabase.from("econoquest_hint_cache").upsert({
      cache_key:      cacheKey,
      hint,
      state_snapshot: stateSnapshot,
      last_used:      new Date().toISOString(),
      hits:           1,
    }, { onConflict: "cache_key" });

  } catch (err) {
    console.error("[cache] setCachedHint error:", err);
  }
}