# Railway infrastructure

`railway.ts` describes the existing `pantry-manager` Railway project: the
GitHub-backed service, build and runtime settings, single replica, persistent
`food-data` volume and its `/data` mount. Railway-generated domains remain
managed by Railway. The file targets the existing production project and is not
a generic template for a new deployment.

The service uses Railway's default `ON_FAILURE` restart policy, with the
existing five-retry limit declared in the IaC file.

## Review and apply

Install Node.js 22 or later and Railway CLI 5.71.0 or later, authenticate, and
link this checkout to the intended Railway project and environment. Then run:

```sh
npm ci --prefix .railway
railway status
railway config plan
# After reviewing the plan:
railway config apply
```

Check the project and environment in `railway status` before planning or
applying. The plan should retain the existing `food-data` volume and all
intended variables. Review every change, especially volume or variable
removals. A push of `railway.ts` does not apply it: Railway builds application
revisions from `master` separately from the IaC plan/apply workflow.

On Windows, npm's PowerShell launcher may cause the SDK's CLI version check to
fail even with a current CLI. If that happens with a global npm installation,
point the process-local `_` variable at the installed executable before
running the Railway commands:

```powershell
$env:_ = Join-Path (npm root -g) '@railway/cli/bin/railway.exe'
railway config plan
```

## Variables and secrets

The project manages variable **names** in `railway.ts`. Each `preserve()`
keeps the corresponding existing Railway value without storing it in Git.
Because `variables.managed` is enabled, applying a plan can remove service
variables absent from the file. When adding a variable, set its value in
Railway and add its name with `preserve()` before the next apply. Remove a name
only when the corresponding Railway variable should also be removed. Never
commit provider keys, bot tokens, or decrypted plan artifacts.

The authoring file captures the current project and region. To use it for a
different installation, adjust those identities, repository, region, and
variables for that installation and review its plan before applying.
