% rebase('base', title='Error')

<div class="page-header">
    <h1 class="title">Error: Block {{ block_id }} Not Found</h1>
    <hr />
</div>

<p>The block you are looking for doesn't seem to exist!</p>
<p>
    There are a few reasons why that might be the case:
    <ol>
        <li>It may be from an older sheet that is no longer active</li>
        <li>It may be the wrong ID - are you sure block {{ block_id }} is the one you want?</li>
        % alt_systems = [s for s in systems if s.get_block(block_id) is not None]
        % if len(alt_systems) > 0:
            <li>
                It may be from a different system - the following systems have a block with that ID
                <ul>
                    % for alt_system in alt_systems:
                        <li>{{ alt_system }}: <a href="{{ get_url(alt_system, f'blocks/{block_id}') }}">Block {{ block_id }}</a></li>
                    % end
                </ul>
            </li>
        % end
    </ol>
</p>

<p>
    If you believe this error is incorrect and the block actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!
</p>

<p>
    <button class="button" onclick="window.history.back()">Back</button>
</p>
