
% rebase('base')

<div id="page-header">
    <h1>Vehicle History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'history') }}" class="tab-button">Last Seen</a>
        <a href="{{ get_url(system, 'history/first-seen') }}" class="tab-button">First Seen</a>
        <span class="tab-button current">Transfers</span>
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        % if system:
            <div class="section closed">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Filters</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="info-box">
                        <div class="section">
                            <div class="options-container">
                                <div class="option" onclick="setFilter(null)">
                                    <div class="radio-button {{ '' if filter else 'selected' }}"></div>
                                    <div>All Transfers</div>
                                </div>
                                <div class="option" onclick="setFilter('from')">
                                    <div class="radio-button {{ 'selected' if filter == 'from' else '' }}"></div>
                                    <div>From {{ system }}</div>
                                </div>
                                <div class="option" onclick="setFilter('to')">
                                    <div class="radio-button {{ 'selected' if filter == 'to' else '' }}"></div>
                                    <div>To {{ system }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <script>
                        function setFilter(filter) {
                            if (filter === null) {
                                window.location = "{{ get_url(system, 'history/transfers') }}";
                            } else {
                                window.location = "{{ get_url(system, 'history/transfers') }}?filter=" + filter;
                            }
                        }
                    </script>
                </div>
            </div>
        % end
        % if transfers:
            <div class="section closed">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Statistics</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % models = sorted({t.bus.model for t in transfers if t.bus.model})
                    % model_types = sorted({m.type for m in models})
                    <table>
                        <thead>
                            <tr>
                                <th>Model</th>
                                <th class="align-right">Count</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for model_type in model_types:
                                % type_transfers = [t for t in transfers if t.bus.model and t.bus.model.type == model_type]
                                <tr class="header">
                                    <td>{{ model_type }}</td>
                                    <td class="align-right">{{ len(type_transfers) }}</td>
                                </tr>
                                <tr class="display-none"></tr>
                                % type_models = [m for m in models if m.type == model_type]
                                % for model in type_models:
                                    % model_transfers = [t for t in type_transfers if t.bus.model == model]
                                    <tr>
                                        <td>{{! model }}</td>
                                        <td class="align-right">{{ len(model_transfers) }}</td>
                                    </tr>
                                % end
                            % end
                            <tr class="header">
                                <td>Total</td>
                                <td class="align-right">{{ len(transfers) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        % end
    </div>
    <div class="container flex-3">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Transfers</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if transfers:
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Bus</th>
                                <th class="desktop-only">Model</th>
                                <th class="non-mobile">From</th>
                                <th class="non-mobile">To</th>
                                <th class="mobile-only">Systems</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_date = None
                            % for transfer in transfers:
                                % bus = transfer.bus
                                % same_date = last_date is None or transfer.date == last_date
                                % last_date = transfer.date
                                <tr class="{{'' if same_date else 'divider'}}">
                                    <td class="desktop-only">{{ transfer.date.format_long() }}</td>
                                    <td class="non-desktop">{{ transfer.date.format_short() }}</td>
                                    <td>
                                        <div class="column">
                                            % include('components/bus')
                                            <span class="non-desktop smaller-font">
                                                % include('components/order', order=bus.order)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/order', order=bus.order)
                                    </td>
                                    <td class="non-mobile">{{ transfer.old_system }}</td>
                                    <td class="non-mobile">{{ transfer.new_system }}</td>
                                    <td class="mobile-only">
                                        <div class="column">
                                            <div>
                                                <div class="smaller-font">From:</div>
                                                {{ transfer.old_system }}
                                            </div>
                                            <div>
                                                <div class="smaller-font">To:</div>
                                                {{ transfer.new_system }}
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                % else:
                    <div class="placeholder">
                        % if system is None:
                            <h3>No transfers found</h3>
                            <p>Something has probably gone terribly wrong if you're seeing this.</p>
                        % elif not system.realtime_enabled:
                            <h3>{{ system }} does not currently support realtime</h3>
                            <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
                            <div class="non-desktop">
                                % include('components/systems')
                            </div>
                        % elif filter == 'from':
                            <h3>No buses have been transferred from {{ system }}</h3>
                            <p>Please choose a different filter or check again later!</p>
                        % elif filter == 'to':
                            <h3>No buses have been transferred to {{ system }}</h3>
                            <p>Please choose a different filter or check again later!</p>
                        % else:
                            <h3>No buses have been transferred to or from {{ system }}</h3>
                            <p>Please check again later!</p>
                        % end
                    </div>
                % end
            </div>
        </div>        
    </div>
</div>

% include('components/top_button')
