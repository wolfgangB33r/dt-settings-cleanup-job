# Dynatrace Settings Cleanup Job

A stateless cleanup job for Dynatrace settings schemas.

This job automatically iterates through all the settings entries of any given Dynatrace settings schema and
deletes entries that were not modified since a configurable period of time.

This job can be used to reset and clean a Dynatrace test environment by removing settings entries that
might mess up an environment.

Used as a cron triggered job, this job helps to automatically keep a Dynatrace test environment clean. 

This job is not meant for modifying Dynatrace production environments.

## Necessary Configuration

In order to use this job, following settings need to be set as environment variables:

- KEEP_PERIOD_DAYS (default = 14 days), e.g.: 14
- DYNATRACE_API_TOKEN: An API token secret that has the permission (settings.read, settings.write) to read and write your configured settings schemas.
- DYNATRACE_ENVIRONMENT_URL: The domain of your Dynatrace environment e.g.: http://abc234112.live.dynatrace.com
- SETTINGS_SCHEMAS: Comma separated list of settings schemas to cleanup e.g.: builtin:anomaly-detection.metric-events,builtin:alerting.profile,builtin:alerting.maintenance-window,builtin:problem.notifications,builtin:infrastructure.disk.edge.anomaly-detectors,builtin:davis.anomaly-detectors
