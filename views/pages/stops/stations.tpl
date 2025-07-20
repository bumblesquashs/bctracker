
% rebase('base')

<div id="page-header">
    <h1>Stations</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'stops') }}" class="tab-button">Stops</a>
        <span class="tab-button current">Stations</span>
    </div>
</div>

% if context.system:
    <div class="container">
        <div class="section">
            <div class="content">
                % if stops:
                    <table>
                        <thead>
                            <tr>
                                <th>Station</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for stop in stops:
                                <tr>
                                    <td>
                                        % include('components/stop')
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                    
                    % include('components/top_button')
                % else:
                    <div class="placeholder">
                        <h3>{{ context }} station information is unavailable</h3>
                        % if context.gtfs_loaded:
                            <p>Please check again later!</p>
                        % else:
                            <p>System data is currently loading and will be available soon.</p>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
% else:
    <div class="placeholder">
        <p>Choose a system to see individual stations.</p>
        <div class="non-desktop">
            % include('components/systems')
        </div>
    </div>
% end
