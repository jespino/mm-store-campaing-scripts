Mattermost is migrating its Store layer to be sync by default, and only use Async when needed and we're looking for contributors to help with that effort. This Help Wanted issue is to migrate the `{{method}}` in the `{{store}}` store.

The expected way to implement it is, go to the `{{store}}` store implementation in the `store/sqlstore/` directory, modify the method `{{method}}` to return directly an object from the `model` module, and a `*model.AppError` (removing the `store.Do` wrapper). After that, you must modify the interface defined in `store/store.go` to match with the changes. Then, you should execute `make store-mocks` to rebuild the mocks with the new interface. And finally, modify the rest of the code (tests included) to use the new interface of the function properly.

Example: mattermost/mattermost-server#10613
