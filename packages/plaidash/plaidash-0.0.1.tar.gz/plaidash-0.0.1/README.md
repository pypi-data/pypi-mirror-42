# Plaidash LoginForm
The purpose of this project is to create a dash component for the plaid link for easy rendering and use 
with python once an `access_token` is retrieved.

![alt text](https://github.com/SterlingButters/plaidash/blob/master/PlaidDemo.gif)

### Structure 
- The demo app is in `src/demo`; component is imported to demo app.
- Component written in `src/lib/components/LoginForm.react.js`

### Acknowledgements
A special thanks to:
 [@tcbegley](https://community.plot.ly/u/tcbegley)
 [@pbernasconi](https://github.com/pbernasconi/react-plaid-link)



# TODO:

        
##### Sample Usage:

    # https://plaid.com/docs/#exchange-token-flow
    from dash.dependencies import Input, Output, State
    import dash_html_components as html
    import dash
    import json
    import plaid
    import os
    import plaidash
    import datetime
    from flask import jsonify
    
    app = dash.Dash(__name__)
    app.config['suppress_callback_exceptions'] = True
    
    app.layout = html.Div([
        html.Div(id='login-container'),
        html.Button('Open Plaid', id='open-form-button'),
    ])
    
    with open('/Users/sterlingbutters/.plaid/.credentials.json') as CREDENTIALS:
        KEYS = json.load(CREDENTIALS)
        print(json.dumps(KEYS, indent=2))
    
        PLAID_CLIENT_ID = KEYS['client_id']
        PLAID_PUBLIC_KEY = KEYS['public_key']
        ENV = 'sandbox'
        if ENV == 'sandbox':
            PLAID_SECRET = KEYS['sandbox_secret']
        if ENV == 'dvelopment':
            PLAID_SECRET = KEYS['development_secret']
        PLAID_ENV = os.getenv('PLAID_ENV', ENV)
        PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', ['auth', 'transactions'])
    
    client = plaid.Client(client_id=PLAID_CLIENT_ID,
                          secret=PLAID_SECRET,
                          public_key=PLAID_PUBLIC_KEY,
                          environment=PLAID_ENV,
                          api_version='2018-05-22')
    
    
    @app.callback(Output('login-container', 'children'),
                  [Input('open-form-button', 'n_clicks'),])
    def display_output(clicks):
        if clicks is not None and clicks > 0:
            return html.Div([
                plaidash.LoginForm(
                id='plaid-link',
                clientName='Butters',
                env=PLAID_ENV,
                publicKey=PLAID_PUBLIC_KEY,
                product=PLAID_PRODUCTS,
                # institution=
            ),
                html.Button('Load Transactions', id='load-button'),
                html.Div(id='display-transactions'),
            ])
    
    
    @app.callback(Output('display-transactions', 'children'),
                 [Input('load-button', 'n_clicks')],
                 [State('plaid-link', 'public_token')])
    def display_output(clicks, public_token):
        if clicks is not None and clicks > 0:
            print(public_token)
            response = client.Item.public_token.exchange(public_token)
            access_token = response['access_token']
            print(access_token)
    
            start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-30))
            end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
            try:
                transactions_response = client.Transactions.get(access_token=access_token, start_date=start_date, end_date=end_date)
            except plaid.errors.PlaidError as e:
                # return html.P(jsonify(format_error(e)))
                return html.P('There was an error')
    
            print(pretty_response(transactions_response))
            # return html.P(str(jsonify({'error': None, 'transactions': transactions_response})))
            return html.P(pretty_response(transactions_response))
    
    
    def pretty_response(response):
        return json.dumps(response, indent=2, sort_keys=True)
    
    
    def format_error(e):
        return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type,}} # 'error_message': e.message } }
    
    
    if __name__ == '__main__':
        app.run_server(debug=True, dev_tools_hot_reload=False)

##### Credentials File:
    {
      "client_id": "************************",
      "public_key": "******************************",
      "development_secret": "******************************",
      "sandbox_secret": "******************************",
      "production_secret": ""
    }

## Contributing
- Write tests for the component.
    - A sample test is available in `tests/test_usage.py`, it will load `usage.py` and you can then automate interactions 
    with selenium.
    - Run the tests with `$ pytest tests`.
    - The Dash team uses these types of integration tests extensively. Browse the Dash component code on GitHub for more 
    examples of testing (e.g. https://github.com/plotly/dash-core-components)
- Add custom styles to by putting custom CSS files into distribution folder (`plaidash`).
    - Make sure that they are referenced in `MANIFEST.in` so that they get properly included when ready to publish component.
    - Make sure the stylesheets are added to the `_css_dist` dict in `plaidash/__init__.py` so dash will serve them automatically 
    when the component suite is requested.
- [Review your code](./review_checklist.md)
- Test your code in a Python environment:
    1. Build your code
        ```
        $ npm run build:all
        ```
    2. Run and modify the `usage.py` sample dash app:
        ```
        $ python usage.py
        ```

### Create a production build and publish:
1. Build your code:
    ```
    $ npm run build:all
    ```
2. Create a Python tarball
    ```
    $ python setup.py sdist
    ```
    This distribution tarball will get generated in the `dist/` folder

3. Test your tarball by copying it into a new environment and installing it locally:
    ```
    $ pip install plaidash-0.0.1.tar.gz
    ```

4. If it works, then you can publish the component to NPM and PyPI:
    1. Cleanup the dist folder (optional)
        ```
        $ rm -rf dist
        ```
    2. Publish on PyPI
        ```
        $ twine upload dist/*
        ```
    3. Publish on NPM (Optional if chosen False in `publish_on_npm`)
        ```
        $ npm publish
        ```
        _Publishing your component to NPM will make the JavaScript bundles available on the unpkg CDN. By default, Dash servers the component library's CSS and JS from the remote unpkg CDN, so if you haven't published the component package to NPM you'll need to set the `serve_locally` flags to `True` (unless you choose `False` on `publish_on_npm`). We will eventually make `serve_locally=True` the default, [follow our progress in this issue](https://github.com/plotly/dash/issues/284)._
