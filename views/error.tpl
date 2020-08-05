% include('templates/header', title='Error: {0}'.format(error))

<style>
    #error-block {
        text-align: center;
        margin-top: 50px;
    }
    #error-title {
        font-size: 48pt;
    }
    #error-message {
        font-size: 24pt;
    }
</style>

<div id="error-block">
    <p id="error-title">Error: {{ error }}</p>

    % if defined('message'):
        <p id="error-message">{{ message }}</p>
    % end
</div>

% include('templates/footer')
