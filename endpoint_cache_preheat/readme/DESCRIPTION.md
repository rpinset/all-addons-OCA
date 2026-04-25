Delay cache pre-heat for expensive endpoints.

If an endpoint takes to long to get cached, it will probably make your
call fail or any cron job that calls it.

This module allows pre-heat the cache and delay its generation.
