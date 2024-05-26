
% dates = sorted({e.date for e in events}, reverse=True)

<div class="events">
    % for date in dates:
        <div class="date">
            <div class="tooltip-anchor">
                <div class="row gap-5">
                    % include('components/svg', name='calendar')
                    <div>{{ date }}</div>
                </div>
                <div class="tooltip right">{{ date.format_since() }}</div>
            </div>
        </div>
        <div class="content">
            <ul>
                % date_events = [e for e in events if e.date == date]
                % for event in date_events:
                    <li class="event">
                        <div class="column gap-0">
                            <div>{{ event.name }}</div>
                            % if event.description:
                                <div class="smaller-font lighter-text">{{ event.description }}</div>
                            % end
                        </div>
                    </li>
                % end
            </ul>
        </div>
    % end
</div>
