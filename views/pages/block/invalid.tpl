
% rebase('base')

<div id="page-header">
    <h1>Block {{ block_id }} Not Found</h1>
</div>

<div class="placeholder">
    <h3>The block you are looking for doesn't seem to exist!</h3>
    % if context.gtfs_loaded:
        <p>There are a few reasons why that might be the case:</p>
        <ol>
            <li>It may be from an older sheet that is no longer active</li>
            <li>It may be the wrong ID - are you sure block <b>{{ block_id }}</b> is the one you want?</li>
            % if alt_blocks:
                <li>
                    It may be from a different system - the following systems have a block with that ID
                    <ul>
                        % for block in alt_blocks:
                            <li>{{ block.context }}: <a href="{{ block.url() }}">Block {{ block.id }}</a></li>
                        % end
                    </ul>
                </li>
            % end
        </ol>
        <p>If you believe this error is incorrect and the block actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!</p>

        <button class="button" onclick="window.history.back()">Back</button>
    % else:
        <p>System data is currently loading and will be available soon.</p>
    % end
</div>
