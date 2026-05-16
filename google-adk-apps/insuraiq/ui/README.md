# InsuraIQ UI

Ui for our solution InsuraIQ.

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 20.0.3.

## Prerequisites

- client id for google sign in.
- Multi agent system in vertex agent engine.

## Set up your environment file

Add the following values

- googleClientId: 'YOUR_CLIENT_ID',
- project_id: 'YOUR_GOOGLE_CLOUD_PROJECT_ID',
- location: 'LOCATION',
- reasoning_engine: 'DEPLOYED_AGENT_ENGINE_RESOURCE_ID',
- backend_url: 'https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/LOCATION/reasoningEngines/{reasoning_engine}'

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
